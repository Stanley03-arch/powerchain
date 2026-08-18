from __future__ import annotations

from typing import Dict, List, Optional

from powerchain.core.models.base import ChatMessage, Role


class SharedMemory:
    """Simple shared memory that all agents in a crew can read/write.

    Stores:
    - A running log of contributions
    - Key-value facts that agents can publish
    """

    def __init__(self):
        self.log: List[str] = []
        self.facts: Dict[str, str] = {}

    def add(self, agent_name: str, content: str) -> None:
        entry = f"[{agent_name}]: {content}"
        self.log.append(entry)

    def set_fact(self, key: str, value: str) -> None:
        self.facts[key] = value

    def get_fact(self, key: str) -> Optional[str]:
        return self.facts.get(key)

    def get_context(self, max_entries: int = 20) -> str:
        """Return a string context for agents."""
        parts = []
        if self.facts:
            facts_str = "\n".join(f"- {k}: {v}" for k, v in self.facts.items())
            parts.append(f"Known facts:\n{facts_str}")
        if self.log:
            recent = self.log[-max_entries:]
            parts.append("Recent contributions:\n" + "\n".join(recent))
        return "\n\n".join(parts) if parts else "No shared context yet."

    def clear(self) -> None:
        self.log.clear()
        self.facts.clear()
