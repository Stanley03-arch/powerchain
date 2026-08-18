from __future__ import annotations

import os
from typing import Any, List, Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role


class ChatOpenAI(BaseChatModel):
    """OpenAI-compatible chat model.

    Works with OpenAI, Azure OpenAI, and any OpenAI-compatible endpoint
    (Groq, Together, Fireworks, local vLLM, etc.).
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ):
        self.model_name = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra = kwargs

        try:
            from openai import OpenAI, AsyncOpenAI
        except ImportError as e:
            raise ImportError(
                "openai package is required. Install with: pip install powerchain[openai]"
            ) from e

        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self._client = OpenAI(**client_kwargs)
        self._async_client = AsyncOpenAI(**client_kwargs)

    def _prepare_messages(self, messages: List[ChatMessage]) -> list[dict]:
        return [m.to_dict() for m in messages]

    def invoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        params: dict[str, Any] = {
            "model": self.model_name,
            "messages": self._prepare_messages(messages),
            "temperature": self.temperature,
            **self.extra,
            **kwargs,
        }
        if self.max_tokens is not None:
            params["max_tokens"] = self.max_tokens
        if tools:
            params["tools"] = tools

        response = self._client.chat.completions.create(**params)
        choice = response.choices[0].message

        tool_calls = None
        if choice.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in choice.tool_calls
            ]

        return ChatMessage(
            role=Role.ASSISTANT,
            content=choice.content or "",
            tool_calls=tool_calls,
        )

    async def ainvoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        params: dict[str, Any] = {
            "model": self.model_name,
            "messages": self._prepare_messages(messages),
            "temperature": self.temperature,
            **self.extra,
            **kwargs,
        }
        if self.max_tokens is not None:
            params["max_tokens"] = self.max_tokens
        if tools:
            params["tools"] = tools

        response = await self._async_client.chat.completions.create(**params)
        choice = response.choices[0].message

        tool_calls = None
        if choice.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in choice.tool_calls
            ]

        return ChatMessage(
            role=Role.ASSISTANT,
            content=choice.content or "",
            tool_calls=tool_calls,
        )
