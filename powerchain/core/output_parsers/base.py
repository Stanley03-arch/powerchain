from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseOutputParser(ABC, Generic[T]):
    """Base class for output parsers."""

    @abstractmethod
    def parse(self, text: str) -> T:
        """Parse the LLM output into a structured form."""
        ...

    def try_parse(self, text: str) -> T | None:
        try:
            return self.parse(text)
        except Exception:
            return None
