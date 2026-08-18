from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, AsyncIterator, Iterator, List, Optional, Union

from pydantic import BaseModel, Field


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ChatMessage(BaseModel):
    role: Role
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[dict]] = None

    def to_dict(self) -> dict:
        data = {"role": self.role.value, "content": self.content}
        if self.name:
            data["name"] = self.name
        if self.tool_call_id:
            data["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            data["tool_calls"] = self.tool_calls
        return data


class BaseChatModel(ABC):
    """Unified interface for chat models."""

    model_name: str = "unknown"

    @abstractmethod
    def invoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        """Synchronous generation."""
        ...

    @abstractmethod
    async def ainvoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        """Asynchronous generation."""
        ...

    def stream(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        """Synchronous streaming (default falls back to full response)."""
        result = self.invoke(messages, tools=tools, **kwargs)
        yield result.content

    async def astream(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """Asynchronous streaming."""
        result = await self.ainvoke(messages, tools=tools, **kwargs)
        yield result.content
