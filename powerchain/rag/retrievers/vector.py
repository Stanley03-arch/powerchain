from __future__ import annotations

from typing import List

from powerchain.rag.documents import Document
from powerchain.rag.retrievers.base import BaseRetriever
from powerchain.rag.vectorstores.base import VectorStore


class VectorStoreRetriever(BaseRetriever):
    """Retriever that uses a VectorStore."""

    def __init__(self, vectorstore: VectorStore, search_kwargs: dict | None = None):
        self.vectorstore = vectorstore
        self.search_kwargs = search_kwargs or {"k": 4}

    def get_relevant_documents(self, query: str) -> List[Document]:
        return self.vectorstore.similarity_search(query, **self.search_kwargs)
