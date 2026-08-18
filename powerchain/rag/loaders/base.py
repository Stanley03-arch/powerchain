from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from powerchain.rag.documents import Document


class BaseLoader(ABC):
    """Base class for document loaders."""

    @abstractmethod
    def load(self) -> List[Document]:
        """Load data into a list of Documents."""
        ...

    def load_and_split(self, splitter) -> List[Document]:
        """Load and then split the documents."""
        docs = self.load()
        return splitter.split_documents(docs)
