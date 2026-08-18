from __future__ import annotations

from typing import Any, List, Optional

from powerchain.core.agents.agent import Agent
from powerchain.core.models.base import BaseChatModel
from powerchain.core.tools.base import BaseTool
from powerchain.core.memory.conversation import ConversationMemory


class AgentNode:
    """A named agent that can be used inside a Crew or Graph."""

    def __init__(
        self,
        name: str,
        llm: BaseChatModel,
        role: str = "Helpful assistant",
        goal: str = "Complete the given task accurately",
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[ConversationMemory] = None,
        system_prompt: Optional[str] = None,
        max_iterations: int = 6,
    ):
        self.name = name
        self.role = role
        self.goal = goal

        prompt = system_prompt or (
            f"You are {name}.\n"
            f"Role: {role}\n"
            f"Goal: {goal}\n\n"
            "Be concise, accurate, and collaborative. "
            "Use tools when they help you."
        )

        self.agent = Agent(
            llm=llm,
            tools=tools or [],
            memory=memory or ConversationMemory(),
            system_prompt=prompt,
            max_iterations=max_iterations,
        )

    def run(self, task: str) -> str:
        return self.agent.run(task)

    async def arun(self, task: str) -> str:
        return await self.agent.arun(task)

    def __repr__(self) -> str:
        return f"AgentNode(name={self.name!r}, role={self.role!r})"
