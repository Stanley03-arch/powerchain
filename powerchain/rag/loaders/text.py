from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

from powerchain.rag.documents import Document
from powerchain.rag.loaders.base import BaseLoader


class TextLoader(BaseLoader):
    """Load a plain text file."""

    def __init__(self, file_path: Union[str, Path], encoding: str = "utf-8"):
        self.file_path = Path(file_path)
        self.encoding = encoding

    def load(self) -> List[Document]:
        text = self.file_path.read_text(encoding=self.encoding)
        return [
            Document(
                page_content=text,
                metadata={"source": str(self.file_path)},
            )
        ]
