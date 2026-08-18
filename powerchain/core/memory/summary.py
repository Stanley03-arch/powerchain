from __future__ import annotations

from typing import List, Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.memory.conversation import ConversationMemory


class SummaryMemory(ConversationMemory):
    """Conversation memory that automatically summarizes older messages
    when the history grows too long.

    Keeps recent messages intact + a running summary of the past.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        max_messages: int = 12,
        summarize_threshold: int = 10,
        summary_prompt: Optional[str] = None,
    ):
        super().__init__(max_messages=max_messages)
        self.llm = llm
        self.summarize_threshold = summarize_threshold
        self.summary: str = ""
        self.summary_prompt = summary_prompt or (
            "Progressively summarize the conversation below. "
            "Keep key facts, decisions, and context. Be concise.\n\n"
            "Current summary:\n{summary}\n\n"
            "New lines:\n{new_lines}\n\n"
            "Updated summary:"
        )

    def add_user(self, content: str) -> None:
        super().add_user(content)
        self._maybe_summarize()

    def add_assistant(self, content: str) -> None:
        super().add_assistant(content)
        self._maybe_summarize()

    def get_messages(self) -> List[ChatMessage]:
        messages: List[ChatMessage] = []
        if self.summary:
            messages.append(
                ChatMessage(
                    role=Role.SYSTEM,
                    content=f"Previous conversation summary:\n{self.summary}",
                )
            )
        messages.extend(self._messages)
        return messages

    def _maybe_summarize(self) -> None:
        if len(self._messages) < self.summarize_threshold:
            return

        # Take older half to summarize
        to_summarize = self._messages[: len(self._messages) // 2]
        keep = self._messages[len(self._messages) // 2 :]

        new_lines = "\n".join(f"{m.role.value}: {m.content}" for m in to_summarize)

        prompt = self.summary_prompt.format(summary=self.summary or "None", new_lines=new_lines)

        response = self.llm.invoke([ChatMessage(role=Role.USER, content=prompt)])
        self.summary = response.content.strip()
        self._messages = keep
