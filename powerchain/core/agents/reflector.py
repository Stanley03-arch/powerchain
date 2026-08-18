from __future__ import annotations

from typing import Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role


class Reflector:
    """Critiques an answer and suggests improvements or confirms quality."""

    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def reflect(self, task: str, answer: str) -> str:
        """Return a reflection / critique of the answer."""
        prompt = (
            "You are a critical but fair reviewer. Evaluate the following answer to the task.\n"
            "Point out any weaknesses, missing information, or errors. "
            "If the answer is already strong, say so clearly.\n\n"
            f"Task: {task}\n\n"
            f"Answer:\n{answer}\n\n"
            "Reflection:"
        )
        response = self.llm.invoke([ChatMessage(role=Role.USER, content=prompt)])
        return response.content.strip()

    def improve(self, task: str, answer: str, reflection: Optional[str] = None) -> str:
        """Produce an improved version of the answer based on reflection."""
        if reflection is None:
            reflection = self.reflect(task, answer)

        prompt = (
            "Improve the answer based on the reflection below. "
            "Return ONLY the improved final answer.\n\n"
            f"Task: {task}\n\n"
            f"Original Answer:\n{answer}\n\n"
            f"Reflection:\n{reflection}\n\n"
            "Improved Answer:"
        )
        response = self.llm.invoke([ChatMessage(role=Role.USER, content=prompt)])
        return response.content.strip()
