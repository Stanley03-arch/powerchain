from __future__ import annotations

from typing import Any, Iterator, List, Optional, Sequence

from powerchain.core.models.base import BaseChatModel, ChatMessage


class FallbackChatModel(BaseChatModel):
    """Try multiple chat models in order until one succeeds.

    Useful for reliability (primary + backup providers).
    """

    def __init__(self, models: Sequence[BaseChatModel], model_name: str = "fallback"):
        if not models:
            raise ValueError("At least one model is required")
        self.models = list(models)
        self.model_name = model_name

    def invoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        last_error = None
        for model in self.models:
            try:
                return model.invoke(messages, tools=tools, **kwargs)
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(f"All models failed. Last error: {last_error}") from last_error

    async def ainvoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        last_error = None
        for model in self.models:
            try:
                return await model.ainvoke(messages, tools=tools, **kwargs)
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(f"All models failed. Last error: {last_error}") from last_error

    def stream(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        last_error = None
        for model in self.models:
            try:
                yield from model.stream(messages, tools=tools, **kwargs)
                return
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(f"All models failed while streaming. Last error: {last_error}") from last_error
