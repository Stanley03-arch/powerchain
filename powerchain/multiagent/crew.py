from __future__ import annotations

from typing import List, Optional

from powerchain.multiagent.agent_node import AgentNode


class Crew:
    """A simple multi-agent crew that can run agents sequentially or in a basic collaboration pattern.

    This is intentionally clean and easy to understand — more powerful patterns
    can be built on top of the Graph system.
    """

    def __init__(self, agents: List[AgentNode], verbose: bool = True):
        self.agents = {a.name: a for a in agents}
        self.verbose = verbose

    def run_sequential(self, task: str) -> str:
        """Pass the task through each agent in order. Each agent sees the previous output."""
        current = task
        for name, agent in self.agents.items():
            if self.verbose:
                print(f"\n▶ [{name}] working...")
            current = agent.run(
                f"Original task: {task}\n\n"
                f"Previous result:\n{current}\n\n"
                f"Your turn. Improve or continue the work."
            )
            if self.verbose:
                print(f"  Result from {name}: {current[:150]}...")
        return current

    def run_single(self, agent_name: str, task: str) -> str:
        """Run only one specific agent."""
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Available: {list(self.agents)}")
        return self.agents[agent_name].run(task)

    def run_round_robin(self, task: str, rounds: int = 2) -> str:
        """Let agents take turns multiple times."""
        current = task
        for r in range(rounds):
            if self.verbose:
                print(f"\n=== Round {r + 1} ===")
            for name, agent in self.agents.items():
                if self.verbose:
                    print(f"▶ [{name}]...")
                current = agent.run(
                    f"Task: {task}\n\nCurrent state:\n{current}\n\n"
                    f"Contribute your expertise."
                )
        return current
