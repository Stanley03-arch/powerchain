from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from powerchain.rag.documents import Document
from powerchain.rag.embeddings.base import Embeddings


class VectorStore(ABC):
    """Abstract vector store."""

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents and return their IDs."""
        ...

    @abstractmethod
    def similarity_search(
        self, query: str, k: int = 4, **kwargs
    ) -> List[Document]:
        """Return the most similar documents."""
        ...

    @abstractmethod
    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs
    ) -> List[Tuple[Document, float]]:
        """Return documents with similarity scores."""
        ...

    def as_retriever(self, search_kwargs: Optional[dict] = None):
        from powerchain.rag.retrievers.vector import VectorStoreRetriever

        return VectorStoreRetriever(vectorstore=self, search_kwargs=search_kwargs or {})
