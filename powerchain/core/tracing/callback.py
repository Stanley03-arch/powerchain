from __future__ import annotations

from typing import Any, Dict, List, Optional


class CallbackHandler:
    """Base callback handler for observability."""

    def on_agent_start(self, input: str, **kwargs: Any) -> None:
        pass

    def on_agent_end(self, output: str, **kwargs: Any) -> None:
        pass

    def on_tool_start(self, tool_name: str, arguments: str, **kwargs: Any) -> None:
        pass

    def on_tool_end(self, tool_name: str, result: str, **kwargs: Any) -> None:
        pass

    def on_llm_start(self, messages: List[Any], **kwargs: Any) -> None:
        pass

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        pass


class ConsoleCallback(CallbackHandler):
    """Simple console logger for debugging."""

    def on_agent_start(self, input: str, **kwargs: Any) -> None:
        print(f"\n[Agent] Starting with: {input[:120]}...")

    def on_agent_end(self, output: str, **kwargs: Any) -> None:
        print(f"[Agent] Finished: {output[:120]}...")

    def on_tool_start(self, tool_name: str, arguments: str, **kwargs: Any) -> None:
        print(f"  → Tool `{tool_name}` called with: {arguments}")

    def on_tool_end(self, tool_name: str, result: str, **kwargs: Any) -> None:
        print(f"  ← Tool `{tool_name}` returned: {result[:100]}")
