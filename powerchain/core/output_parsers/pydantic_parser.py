from __future__ import annotations

import json
import re
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from powerchain.core.output_parsers.base import BaseOutputParser
from powerchain.core.output_parsers.json_parser import JsonOutputParser

T = TypeVar("T", bound=BaseModel)


class PydanticOutputParser(BaseOutputParser[T]):
    """Parse LLM output into a Pydantic model.

    Provides a format instruction you can inject into prompts.
    """

    def __init__(self, model: Type[T]):
        self.model = model
        self._json_parser = JsonOutputParser()

    def get_format_instructions(self) -> str:
        schema = self.model.model_json_schema()
        return (
            "Respond with a valid JSON object that matches this schema:\n"
            f"```json\n{json.dumps(schema, indent=2)}\n```\n"
            "Do not include any text outside the JSON."
        )

    def parse(self, text: str) -> T:
        data = self._json_parser.parse(text)
        try:
            return self.model.model_validate(data)
        except ValidationError as e:
            raise ValueError(f"Pydantic validation failed: {e}") from e
