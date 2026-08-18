from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from powerchain.rag.documents import Document


class TextSplitter(ABC):
    """Base text splitter."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        ...

    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks: List[Document] = []
        for doc in documents:
            texts = self.split_text(doc.page_content)
            for i, text in enumerate(texts):
                metadata = {**doc.metadata, "chunk": i}
                chunks.append(Document(page_content=text, metadata=metadata))
        return chunks
