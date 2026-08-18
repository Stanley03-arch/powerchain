from __future__ import annotations

from typing import Any, Iterator, List, Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from powerchain.core.models.base import BaseChatModel, ChatMessage


class RetryChatModel(BaseChatModel):
    """Wrap any chat model with automatic retries and exponential backoff."""

    def __init__(
        self,
        model: BaseChatModel,
        max_attempts: int = 3,
        min_wait: float = 1.0,
        max_wait: float = 10.0,
    ):
        self.model = model
        self.model_name = f"retry({model.model_name})"
        self.max_attempts = max_attempts
        self.min_wait = min_wait
        self.max_wait = max_wait

    def _retry_decorator(self):
        return retry(
            reraise=True,
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_exponential(multiplier=1, min=self.min_wait, max=self.max_wait),
            retry=retry_if_exception_type(Exception),
        )

    def invoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        @self._retry_decorator()
        def _call():
            return self.model.invoke(messages, tools=tools, **kwargs)

        return _call()

    async def ainvoke(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        # tenacity supports async too
        from tenacity import AsyncRetrying

        async for attempt in AsyncRetrying(
            reraise=True,
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_exponential(multiplier=1, min=self.min_wait, max=self.max_wait),
            retry=retry_if_exception_type(Exception),
        ):
            with attempt:
                return await self.model.ainvoke(messages, tools=tools, **kwargs)

    def stream(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        # Streaming retries are trickier; we retry the whole stream on failure
        @self._retry_decorator()
        def _call():
            return list(self.model.stream(messages, tools=tools, **kwargs))

        for chunk in _call():
            yield chunk
