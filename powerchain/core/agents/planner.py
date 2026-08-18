from __future__ import annotations

from typing import List, Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role


class Planner:
    """Breaks a complex task into a clear sequence of steps."""

    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def plan(self, task: str, context: Optional[str] = None) -> List[str]:
        prompt = (
            "You are an expert planner. Break the following task into a short list of clear, "
            "actionable steps. Return ONLY the steps, one per line, numbered.\n\n"
            f"Task: {task}\n"
        )
        if context:
            prompt += f"\nContext:\n{context}\n"

        response = self.llm.invoke([ChatMessage(role=Role.USER, content=prompt)])
        lines = [line.strip() for line in response.content.strip().splitlines() if line.strip()]

        steps = []
        for line in lines:
            # Remove leading numbers / bullets
            cleaned = line.lstrip("0123456789.-) ").strip()
            if cleaned:
                steps.append(cleaned)

        return steps or [task]
