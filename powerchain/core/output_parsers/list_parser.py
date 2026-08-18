from __future__ import annotations

import re
from typing import List

from powerchain.core.output_parsers.base import BaseOutputParser


class ListOutputParser(BaseOutputParser[List[str]]):
    """Parse a list of items from LLM output (numbered or bulleted)."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().splitlines()
        items = []
        for line in lines:
            cleaned = re.sub(r"^\s*([0-9]+[.)]|[-*+])\s*", "", line).strip()
            if cleaned:
                items.append(cleaned)
        return items or [text.strip()]
