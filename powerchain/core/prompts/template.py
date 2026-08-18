from __future__ import annotations

from typing import Any, Dict


class PromptTemplate:
    """Simple but effective prompt template with {variable} substitution."""

    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs: Any) -> str:
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing variable in prompt template: {e}") from e

    def partial(self, **kwargs: Any) -> "PromptTemplate":
        """Return a new template with some variables already filled."""
        new_template = self.template
        for key, value in kwargs.items():
            new_template = new_template.replace("{" + key + "}", str(value))
        return PromptTemplate(new_template)

    def __str__(self) -> str:
        return self.template
