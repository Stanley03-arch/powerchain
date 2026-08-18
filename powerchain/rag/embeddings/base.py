from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Embeddings(ABC):
    """Interface for embedding models."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        ...

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed a query."""
        ...
