from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Set, Union

from powerchain.rag.documents import Document
from powerchain.rag.loaders.base import BaseLoader
from powerchain.rag.loaders.text import TextLoader


class DirectoryLoader(BaseLoader):
    """Load all matching text files from a directory (optionally recursive)."""

    def __init__(
        self,
        path: Union[str, Path],
        glob: str = "**/*.txt",
        recursive: bool = True,
        encoding: str = "utf-8",
        exclude: Optional[Set[str]] = None,
    ):
        self.path = Path(path)
        self.glob = glob
        self.recursive = recursive
        self.encoding = encoding
        self.exclude = exclude or set()

    def load(self) -> List[Document]:
        if not self.path.exists():
            raise FileNotFoundError(f"Directory not found: {self.path}")

        pattern = self.glob if self.recursive else self.glob.replace("**/", "")
        files = list(self.path.glob(pattern))

        documents: List[Document] = []
        for file_path in files:
            if not file_path.is_file():
                continue
            if file_path.name in self.exclude or str(file_path) in self.exclude:
                continue

            try:
                loader = TextLoader(file_path, encoding=self.encoding)
                documents.extend(loader.load())
            except Exception as e:
                # Skip unreadable files but continue
                print(f"Warning: could not load {file_path}: {e}")

        return documents
