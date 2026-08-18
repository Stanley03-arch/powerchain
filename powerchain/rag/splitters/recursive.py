from __future__ import annotations

from typing import List

from powerchain.rag.splitters.base import TextSplitter


class RecursiveCharacterTextSplitter(TextSplitter):
    """Recursively split text by trying a list of separators."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] | None = None,
    ):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        final_chunks: List[str] = []
        separator = separators[-1]

        for s in separators:
            if s == "":
                separator = s
                break
            if s in text:
                separator = s
                break

        splits = text.split(separator) if separator else list(text)

        good_splits: List[str] = []
        for s in splits:
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:
                if good_splits:
                    merged = self._merge_splits(good_splits, separator)
                    final_chunks.extend(merged)
                    good_splits = []
                if not separators:
                    final_chunks.append(s)
                else:
                    other = self._split_text(s, separators[1:])
                    final_chunks.extend(other)

        if good_splits:
            merged = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged)

        return final_chunks

    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        separator_len = len(separator)
        docs: List[str] = []
        current_doc: List[str] = []
        total = 0

        for d in splits:
            length = len(d)
            if total + length + (separator_len if current_doc else 0) > self.chunk_size:
                if current_doc:
                    doc = separator.join(current_doc)
                    if doc:
                        docs.append(doc)
                    # overlap
                    while total > self.chunk_overlap and current_doc:
                        total -= len(current_doc[0]) + (separator_len if len(current_doc) > 1 else 0)
                        current_doc = current_doc[1:]
            current_doc.append(d)
            total += length + (separator_len if len(current_doc) > 1 else 0)

        if current_doc:
            doc = separator.join(current_doc)
            if doc:
                docs.append(doc)

        return docs
