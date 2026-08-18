from __future__ import annotations

from typing import List

from powerchain.core.models.base import ChatMessage, Role


class ConversationMemory:
    """Simple conversation memory with optional windowing."""

    def __init__(self, max_messages: int = 40):
        self.max_messages = max_messages
        self._messages: List[ChatMessage] = []

    def add_user(self, content: str) -> None:
        self._messages.append(ChatMessage(role=Role.USER, content=content))
        self._trim()

    def add_assistant(self, content: str) -> None:
        self._messages.append(ChatMessage(role=Role.ASSISTANT, content=content))
        self._trim()

    def add_message(self, message: ChatMessage) -> None:
        self._messages.append(message)
        self._trim()

    def get_messages(self) -> List[ChatMessage]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()

    def _trim(self) -> None:
        if len(self._messages) > self.max_messages:
            # Keep the most recent messages
            self._messages = self._messages[-self.max_messages :]
