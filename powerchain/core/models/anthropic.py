from __future__ import annotations

import os
from typing import Any, AsyncIterator, Iterator, List, Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role


class ChatAnthropic(BaseChatModel):
    """Anthropic Claude chat model."""

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs: Any,
    ):
        self.model_name = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra = kwargs

        try:
            from anthropic import Anthropic, AsyncAnthropic
        except ImportError as e:
            raise ImportError(
                "anthropic package required. Install with: pip install anthropic"
            ) from e

        self._client = Anthropic(api_key=self.api_key)
        self._async_client = AsyncAnthropic(api_key=self.api_key)

    def _convert_messages(self, messages: List[ChatMessage]) -> tuple[Optional[str], list[dict]]:
        system = None
        converted = []
        for m in messages:
            if m.role == Role.SYSTEM:
                system = m.content
            else:
                role = "assistant" if m.role == Role.ASSISTANT else "user"
                converted.append({"role": role, "content": m.content})
        return system, converted

    def invoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        system, converted = self._convert_messages(messages)
        params: dict[str, Any] = {
            "model": self.model_name,
            "messages": converted,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            **self.extra,
            **kwargs,
        }
        if system:
            params["system"] = system

        response = self._client.messages.create(**params)
        content = response.content[0].text if response.content else ""
        return ChatMessage(role=Role.ASSISTANT, content=content)

    async def ainvoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        system, converted = self._convert_messages(messages)
        params: dict[str, Any] = {
            "model": self.model_name,
            "messages": converted,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            **self.extra,
            **kwargs,
        }
        if system:
            params["system"] = system

        response = await self._async_client.messages.create(**params)
        content = response.content[0].text if response.content else ""
        return ChatMessage(role=Role.ASSISTANT, content=content)

    def stream(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        system, converted = self._convert_messages(messages)
        params: dict[str, Any] = {
            "model": self.model_name,
            "messages": converted,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            **self.extra,
            **kwargs,
        }
        if system:
            params["system"] = system

        with self._client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                yield text
