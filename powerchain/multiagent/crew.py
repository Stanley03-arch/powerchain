from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from powerchain.multiagent.agent_node import AgentNode
from powerchain.multiagent.shared_memory import SharedMemory


class Crew:
    """Enhanced multi-agent crew with shared memory and multiple execution modes.

    Modes:
    - sequential: one after another (each sees previous output)
    - round_robin: multiple rounds of turn-taking
    - parallel: all agents work independently, then results are combined
    - coordinated: agents share memory and can build on each other's facts
    """

    def __init__(
        self,
        agents: List[AgentNode],
        shared_memory: Optional[SharedMemory] = None,
        verbose: bool = True,
    ):
        self.agents = {a.name: a for a in agents}
        self.shared_memory = shared_memory or SharedMemory()
        self.verbose = verbose

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def run_sequential(self, task: str) -> str:
        """Pass the task through each agent in order."""
        current = task
        for name, agent in self.agents.items():
            self._log(f"\n▶ [{name}] working...")
            prompt = (
                f"Original task: {task}\n\n"
                f"Shared context:\n{self.shared_memory.get_context()}\n\n"
                f"Previous result:\n{current}\n\n"
                f"Your turn. Improve or continue the work as {agent.role}."
            )
            current = agent.run(prompt)
            self.shared_memory.add(name, current)
            self._log(f"  Result from {name}: {current[:150]}...")
        return current

    def run_round_robin(self, task: str, rounds: int = 2) -> str:
        """Agents take turns for multiple rounds."""
        current = task
        for r in range(rounds):
            self._log(f"\n=== Round {r + 1}/{rounds} ===")
            for name, agent in self.agents.items():
                self._log(f"▶ [{name}]...")
                prompt = (
                    f"Task: {task}\n\n"
                    f"Shared context:\n{self.shared_memory.get_context()}\n\n"
                    f"Current state:\n{current}\n\n"
                    f"Contribute your expertise as {agent.role}."
                )
                current = agent.run(prompt)
                self.shared_memory.add(name, current)
        return current

    def run_parallel(self, task: str) -> str:
        """All agents work on the task independently, then results are synthesized."""
        self._log("\n[Crew] Running agents in parallel...")

        def run_one(name: str, agent: AgentNode) -> tuple[str, str]:
            prompt = (
                f"Task: {task}\n\n"
                f"Shared context:\n{self.shared_memory.get_context()}\n\n"
                f"Respond as {agent.role} with goal: {agent.goal}"
            )
            result = agent.run(prompt)
            return name, result

        results = {}
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            futures = {
                executor.submit(run_one, name, agent): name
                for name, agent in self.agents.items()
            }
            for future in as_completed(futures):
                name, result = future.result()
                results[name] = result
                self.shared_memory.add(name, result)
                self._log(f"  ✓ {name} finished")

        # Simple synthesis
        combined = "\n\n".join(f"### {name}\n{res}" for name, res in results.items())
        return combined

    def run_coordinated(self, task: str) -> str:
        """Coordinated mode: agents work sequentially but heavily use shared memory
        and can publish facts for others."""
        self._log("\n[Crew] Coordinated execution with shared memory...")

        for name, agent in self.agents.items():
            self._log(f"\n▶ [{name}] ({agent.role})...")
            prompt = (
                f"You are {name}, role: {agent.role}.\n"
                f"Goal: {agent.goal}\n\n"
                f"Overall task: {task}\n\n"
                f"Shared memory:\n{self.shared_memory.get_context()}\n\n"
                "Contribute your best work. If you discover important facts, "
                "state them clearly so other agents can use them."
            )
            result = agent.run(prompt)
            self.shared_memory.add(name, result)
            self._log(f"  {result[:160]}...")

        # Final synthesis by the last agent (or we could add a dedicated synthesizer)
        final_prompt = (
            f"Original task: {task}\n\n"
            f"All agent contributions:\n{self.shared_memory.get_context()}\n\n"
            "Synthesize the best final answer to the task."
        )
        last_agent = list(self.agents.values())[-1]
        final = last_agent.run(final_prompt)
        return final

    def run_single(self, agent_name: str, task: str) -> str:
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Available: {list(self.agents)}")
        return self.agents[agent_name].run(task)
