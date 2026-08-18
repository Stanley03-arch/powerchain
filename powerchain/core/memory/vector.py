from __future__ import annotations

from typing import List, Optional

from powerchain.core.models.base import ChatMessage, Role
from powerchain.core.memory.conversation import ConversationMemory
from powerchain.rag.documents import Document
from powerchain.rag.embeddings.base import Embeddings
from powerchain.rag.vectorstores.memory import InMemoryVectorStore


class VectorMemory(ConversationMemory):
    """Hybrid memory: recent messages in buffer + long-term vector store.

    When retrieving context, it returns recent messages + most relevant
    past messages from the vector store.
    """

    def __init__(
        self,
        embedding: Embeddings,
        max_recent: int = 8,
        k_long_term: int = 4,
    ):
        super().__init__(max_messages=max_recent)
        self.k_long_term = k_long_term
        self.vectorstore = InMemoryVectorStore(embedding=embedding)
        self._all_messages: List[ChatMessage] = []  # full history for reference

    def add_user(self, content: str) -> None:
        msg = ChatMessage(role=Role.USER, content=content)
        self._messages.append(msg)
        self._all_messages.append(msg)
        self._trim()
        self._index_message(msg)

    def add_assistant(self, content: str) -> None:
        msg = ChatMessage(role=Role.ASSISTANT, content=content)
        self._messages.append(msg)
        self._all_messages.append(msg)
        self._trim()
        self._index_message(msg)

    def _index_message(self, message: ChatMessage) -> None:
        doc = Document(
            page_content=f"{message.role.value}: {message.content}",
            metadata={"role": message.role.value},
        )
        self.vectorstore.add_documents([doc])

    def get_messages(self, query: Optional[str] = None) -> List[ChatMessage]:
        """Return recent messages + relevant long-term memories."""
        messages: List[ChatMessage] = []

        # Long-term relevant context
        if query and self.vectorstore._store:
            relevant = self.vectorstore.similarity_search(query, k=self.k_long_term)
            if relevant:
                context = "\n".join(d.page_content for d in relevant)
                messages.append(
                    ChatMessage(
                        role=Role.SYSTEM,
                        content=f"Relevant past context:\n{context}",
                    )
                )

        # Recent buffer
        messages.extend(self._messages)
        return messages

    def clear(self) -> None:
        super().clear()
        self._all_messages.clear()
        self.vectorstore = InMemoryVectorStore(embedding=self.vectorstore.embedding)
