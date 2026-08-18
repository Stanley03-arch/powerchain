from __future__ import annotations

import uuid
from typing import List, Optional, Tuple

from powerchain.rag.documents import Document
from powerchain.rag.embeddings.base import Embeddings
from powerchain.rag.vectorstores.base import VectorStore


class ChromaVectorStore(VectorStore):
    """Chroma vector store wrapper.

    Requires: pip install chromadb
    """

    def __init__(
        self,
        embedding: Embeddings,
        collection_name: str = "powerchain",
        persist_directory: Optional[str] = None,
    ):
        self.embedding = embedding
        self.collection_name = collection_name

        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            raise ImportError(
                "chromadb is required for ChromaVectorStore. Install with: pip install chromadb"
            ) from e

        if persist_directory:
            self._client = chromadb.PersistentClient(path=persist_directory)
        else:
            self._client = chromadb.Client()

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        if not documents:
            return []

        texts = [d.page_content for d in documents]
        vectors = self.embedding.embed_documents(texts)
        ids = [str(uuid.uuid4()) for _ in documents]
        metadatas = [d.metadata or {} for d in documents]

        self._collection.add(
            ids=ids,
            embeddings=vectors,
            documents=texts,
            metadatas=metadatas,
        )
        return ids

    def similarity_search(self, query: str, k: int = 4, **kwargs) -> List[Document]:
        results = self.similarity_search_with_score(query, k=k, **kwargs)
        return [doc for doc, _ in results]

    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs
    ) -> List[Tuple[Document, float]]:
        query_vec = self.embedding.embed_query(query)

        result = self._collection.query(
            query_embeddings=[query_vec],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        docs_with_scores = []
        if not result["ids"] or not result["ids"][0]:
            return []

        for doc_text, metadata, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        ):
            # Chroma returns distance; convert to similarity-like score
            score = 1.0 - distance if distance is not None else 0.0
            docs_with_scores.append(
                (Document(page_content=doc_text, metadata=metadata or {}), score)
            )

        return docs_with_scores
