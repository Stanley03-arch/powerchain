from __future__ import annotations

import os
from typing import Any, List, Optional

from powerchain.core.models.openai import ChatOpenAI


class ChatGroq(ChatOpenAI):
    """Groq chat model (OpenAI-compatible endpoint).

    Extremely fast inference for supported models.
    """

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ):
        super().__init__(
            model=model,
            api_key=api_key or os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        self.model_name = model
