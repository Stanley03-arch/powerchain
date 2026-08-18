from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A piece of text with optional metadata."""

    page_content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def __str__(self) -> str:
        return self.page_content

    def with_metadata(self, **kwargs: Any) -> "Document":
        new_meta = {**self.metadata, **kwargs}
        return Document(page_content=self.page_content, metadata=new_meta)
