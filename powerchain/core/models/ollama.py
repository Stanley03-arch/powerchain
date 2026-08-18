from __future__ import annotations

from typing import Any, List, Optional

from powerchain.core.models.openai import ChatOpenAI


class ChatOllama(ChatOpenAI):
    """Ollama chat model (local OpenAI-compatible server).

    Default assumes Ollama is running on localhost:11434.
    """

    def __init__(
        self,
        model: str = "llama3.2",
        base_url: str = "http://localhost:11434/v1",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ):
        super().__init__(
            model=model,
            api_key="ollama",  # Ollama ignores the key but OpenAI client requires one
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        self.model_name = model
