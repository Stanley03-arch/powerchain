from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from powerchain.rag.documents import Document


class BaseRetriever(ABC):
    """Base retriever interface."""

    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        ...

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)
