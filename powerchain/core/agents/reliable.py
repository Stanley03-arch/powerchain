from __future__ import annotations

import json
from typing import Any, List, Optional

from powerchain.core.agents.agent import Agent
from powerchain.core.agents.planner import Planner
from powerchain.core.agents.reflector import Reflector
from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.tools.base import BaseTool
from powerchain.core.memory.conversation import ConversationMemory


class ReliableAgent:
    """A significantly more robust agent designed to outperform typical LangChain agents
    on complex tasks through:

    - Explicit planning
    - Step-by-step execution with state tracking
    - Automatic replanning when steps fail
    - Self-reflection + correction
    - Better tool error recovery
    - Optional strict validation
    """

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[ConversationMemory] = None,
        max_steps: int = 8,
        max_replans: int = 2,
        reflect: bool = True,
        verbose: bool = True,
    ):
        self.llm = llm
        self.tools = {t.name: t for t in (tools or [])}
        self.memory = memory or ConversationMemory()
        self.planner = Planner(llm)
        self.reflector = Reflector(llm)
        self.max_steps = max_steps
        self.max_replans = max_replans
        self.reflect = reflect
        self.verbose = verbose

        self._base_agent = Agent(
            llm=llm,
            tools=tools or [],
            memory=ConversationMemory(),  # isolated per step
            max_iterations=5,
        )

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _execute_step(self, step: str, overall_task: str, previous_results: List[str]) -> str:
        """Execute a single step with tool recovery."""
        context = "\n".join(previous_results) if previous_results else "None yet"
        prompt = (
            f"Overall task: {overall_task}\n\n"
            f"Current step: {step}\n\n"
            f"Previous results:\n{context}\n\n"
            "Complete this step carefully. Use tools if needed. "
            "If you cannot complete it, explain why clearly."
        )
        try:
            return self._base_agent.run(prompt)
        except Exception as e:
            return f"STEP_FAILED: {e}"

    def _needs_replan(self, step_result: str) -> bool:
        lower = step_result.lower()
        failure_signals = [
            "step_failed",
            "i cannot",
            "unable to",
            "error",
            "failed",
            "don't know",
            "do not know",
            "insufficient",
        ]
        return any(sig in lower for sig in failure_signals)

    def run(self, task: str) -> str:
        self._log(f"\n{'='*60}\n[ReliableAgent] Starting task:\n{task}\n{'='*60}")

        # 1. Initial plan
        plan = self.planner.plan(task)
        self._log(f"\n[Plan] {len(plan)} steps:")
        for i, s in enumerate(plan, 1):
            self._log(f"  {i}. {s}")

        results: List[str] = []
        replan_count = 0
        step_idx = 0

        while step_idx < len(plan) and step_idx < self.max_steps:
            step = plan[step_idx]
            self._log(f"\n[Step {step_idx + 1}/{len(plan)}] {step}")

            result = self._execute_step(step, task, results)
            self._log(f"  → {result[:200]}{'...' if len(result) > 200 else ''}")

            if self._needs_replan(result) and replan_count < self.max_replans:
                replan_count += 1
                self._log(f"\n[!] Step looks weak — replanning (attempt {replan_count})...")

                # Replan remaining work
                remaining_context = (
                    f"Original task: {task}\n\n"
                    f"Completed so far:\n" + "\n".join(results) + "\n\n"
                    f"Failed / weak step: {step}\nResult: {result}\n\n"
                    "Create a new plan to finish the task from this point."
                )
                new_plan = self.planner.plan(remaining_context)
                plan = plan[:step_idx] + new_plan
                self._log("[New plan]:")
                for i, s in enumerate(new_plan, 1):
                    self._log(f"  {i}. {s}")
                continue  # retry current index with new plan

            results.append(f"Step {step_idx + 1}: {result}")
            step_idx += 1

        # 2. Synthesize final answer
        synthesis_prompt = (
            f"Original task: {task}\n\n"
            f"Results collected:\n" + "\n\n".join(results) + "\n\n"
            "Provide a clear, complete final answer to the original task. "
            "Do not mention the steps — just give the best possible answer."
        )
        final = self._base_agent.run(synthesis_prompt)

        # 3. Optional reflection + improvement
        if self.reflect:
            self._log("\n[Reflection] Critiquing final answer...")
            reflection = self.reflector.reflect(task, final)
            self._log(f"  {reflection[:180]}...")

            if any(w in reflection.lower() for w in ["weak", "missing", "incorrect", "improve", "incomplete", "error"]):
                self._log("[Correction] Improving answer based on reflection...")
                final = self.reflector.improve(task, final, reflection)

        self.memory.add_user(task)
        self.memory.add_assistant(final)

        self._log(f"\n{'='*60}\n[ReliableAgent] Done\n{'='*60}\n")
        return final
