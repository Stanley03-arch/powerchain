from __future__ import annotations

import os
from typing import List, Optional

from powerchain.rag.embeddings.base import Embeddings


class OpenAIEmbeddings(Embeddings):
    """OpenAI embeddings (works with compatible endpoints too)."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")

        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "openai package required. Install with: pip install powerchain[openai]"
            ) from e

        kwargs = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        self._client = OpenAI(**kwargs)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        response = self._client.embeddings.create(model=self.model, input=texts)
        # Ensure order is preserved
        data = sorted(response.data, key=lambda x: x.index)
        return [item.embedding for item in data]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
