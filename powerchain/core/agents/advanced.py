from __future__ import annotations

from typing import List, Optional

from powerchain.core.agents.agent import Agent
from powerchain.core.agents.planner import Planner
from powerchain.core.agents.reflector import Reflector
from powerchain.core.models.base import BaseChatModel
from powerchain.core.tools.base import BaseTool
from powerchain.core.memory.conversation import ConversationMemory


class PlanningAgent:
    """An agent that first creates a plan, then executes step by step.

    Significantly more reliable on complex multi-step tasks.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[ConversationMemory] = None,
        system_prompt: Optional[str] = None,
        max_iterations: int = 6,
    ):
        self.llm = llm
        self.planner = Planner(llm)
        self.agent = Agent(
            llm=llm,
            tools=tools or [],
            memory=memory or ConversationMemory(),
            system_prompt=system_prompt
            or (
                "You are a careful, step-by-step problem solver. "
                "Focus on completing the current step accurately. "
                "Use tools when helpful."
            ),
            max_iterations=max_iterations,
        )

    def run(self, task: str) -> str:
        # 1. Create plan
        steps = self.planner.plan(task)
        print(f"[PlanningAgent] Plan ({len(steps)} steps):")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")

        # 2. Execute each step
        results = []
        for i, step in enumerate(steps, 1):
            print(f"\n[PlanningAgent] Executing step {i}/{len(steps)}: {step}")
            step_prompt = (
                f"Overall task: {task}\n\n"
                f"Current step ({i}/{len(steps)}): {step}\n\n"
                f"Previous results:\n{chr(10).join(results) if results else 'None'}\n\n"
                "Complete this step."
            )
            result = self.agent.run(step_prompt)
            results.append(f"Step {i}: {result}")

        # 3. Synthesize final answer
        synthesis_prompt = (
            f"Original task: {task}\n\n"
            f"Results from each step:\n{chr(10).join(results)}\n\n"
            "Provide a clear final answer to the original task."
        )
        final = self.agent.run(synthesis_prompt)
        return final


class ReflectiveAgent:
    """An agent that answers, reflects on its answer, and improves it."""

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[ConversationMemory] = None,
        max_iterations: int = 6,
        reflect_and_improve: bool = True,
    ):
        self.agent = Agent(
            llm=llm,
            tools=tools or [],
            memory=memory or ConversationMemory(),
            max_iterations=max_iterations,
        )
        self.reflector = Reflector(llm)
        self.reflect_and_improve = reflect_and_improve

    def run(self, task: str) -> str:
        # 1. First attempt
        answer = self.agent.run(task)

        if not self.reflect_and_improve:
            return answer

        # 2. Reflect
        reflection = self.reflector.reflect(task, answer)
        print(f"[ReflectiveAgent] Reflection:\n{reflection}\n")

        # 3. Improve
        improved = self.reflector.improve(task, answer, reflection)
        return improved
