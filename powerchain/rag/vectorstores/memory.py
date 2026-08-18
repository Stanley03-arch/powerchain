from __future__ import annotations

import math
import uuid
from typing import List, Optional, Tuple

from powerchain.rag.documents import Document
from powerchain.rag.embeddings.base import Embeddings
from powerchain.rag.vectorstores.base import VectorStore


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class InMemoryVectorStore(VectorStore):
    """Simple in-memory vector store using cosine similarity.

    Great for prototypes and small corpora. Not for production scale.
    """

    def __init__(self, embedding: Embeddings):
        self.embedding = embedding
        self._store: List[Tuple[str, Document, List[float]]] = []  # id, doc, vector

    def add_documents(self, documents: List[Document]) -> List[str]:
        texts = [d.page_content for d in documents]
        vectors = self.embedding.embed_documents(texts)
        ids = []
        for doc, vector in zip(documents, vectors):
            doc_id = str(uuid.uuid4())
            self._store.append((doc_id, doc, vector))
            ids.append(doc_id)
        return ids

    def similarity_search(self, query: str, k: int = 4, **kwargs) -> List[Document]:
        results = self.similarity_search_with_score(query, k=k, **kwargs)
        return [doc for doc, _ in results]

    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs
    ) -> List[Tuple[Document, float]]:
        if not self._store:
            return []

        query_vec = self.embedding.embed_query(query)
        scored = []
        for _, doc, vec in self._store:
            score = _cosine_similarity(query_vec, vec)
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
