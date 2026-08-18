from __future__ import annotations

import uuid
from typing import List, Optional, Tuple

from powerchain.rag.documents import Document
from powerchain.rag.embeddings.base import Embeddings
from powerchain.rag.vectorstores.base import VectorStore


class FAISSVectorStore(VectorStore):
    """FAISS-based vector store for efficient similarity search.

    Requires: pip install faiss-cpu  (or faiss-gpu)
    """

    def __init__(self, embedding: Embeddings, index=None):
        self.embedding = embedding
        self._docs: List[Document] = []
        self._ids: List[str] = []
        self._index = index  # faiss index, created lazily

        try:
            import faiss
            import numpy as np
            self._faiss = faiss
            self._np = np
        except ImportError as e:
            raise ImportError(
                "faiss is required for FAISSVectorStore. Install with: pip install faiss-cpu"
            ) from e

    def _ensure_index(self, dim: int):
        if self._index is None:
            self._index = self._faiss.IndexFlatIP(dim)  # inner product (cosine after normalization)

    def add_documents(self, documents: List[Document]) -> List[str]:
        if not documents:
            return []

        texts = [d.page_content for d in documents]
        vectors = self.embedding.embed_documents(texts)
        np_vectors = self._np.array(vectors, dtype=self._np.float32)

        # Normalize for cosine similarity via inner product
        self._faiss.normalize_L2(np_vectors)

        self._ensure_index(np_vectors.shape[1])
        self._index.add(np_vectors)

        ids = []
        for doc in documents:
            doc_id = str(uuid.uuid4())
            self._docs.append(doc)
            self._ids.append(doc_id)
            ids.append(doc_id)

        return ids

    def similarity_search(self, query: str, k: int = 4, **kwargs) -> List[Document]:
        results = self.similarity_search_with_score(query, k=k, **kwargs)
        return [doc for doc, _ in results]

    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs
    ) -> List[Tuple[Document, float]]:
        if not self._docs or self._index is None:
            return []

        query_vec = self.embedding.embed_query(query)
        np_query = self._np.array([query_vec], dtype=self._np.float32)
        self._faiss.normalize_L2(np_query)

        k = min(k, len(self._docs))
        scores, indices = self._index.search(np_query, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            results.append((self._docs[idx], float(score)))
        return results

    def save_local(self, folder_path: str) -> None:
        """Save index and documents to disk."""
        import json
        from pathlib import Path

        path = Path(folder_path)
        path.mkdir(parents=True, exist_ok=True)

        self._faiss.write_index(self._index, str(path / "index.faiss"))

        meta = {
            "ids": self._ids,
            "documents": [d.model_dump() for d in self._docs],
        }
        (path / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    @classmethod
    def load_local(cls, folder_path: str, embedding: Embeddings) -> "FAISSVectorStore":
        """Load a previously saved FAISS store."""
        import json
        from pathlib import Path

        path = Path(folder_path)
        import faiss

        index = faiss.read_index(str(path / "index.faiss"))
        meta = json.loads((path / "meta.json").read_text())

        store = cls(embedding=embedding, index=index)
        store._ids = meta["ids"]
        store._docs = [Document(**d) for d in meta["documents"]]
        return store
