from __future__ import annotations

import json
import re
from typing import Any, Dict

from powerchain.core.output_parsers.base import BaseOutputParser


class JsonOutputParser(BaseOutputParser[Dict[str, Any]]):
    """Parse LLM output into a JSON object.

    Handles common cases where the model wraps JSON in markdown code blocks.
    """

    def parse(self, text: str) -> Dict[str, Any]:
        cleaned = text.strip()

        # Extract from markdown code block if present
        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)```", cleaned)
        if code_block:
            cleaned = code_block.group(1).strip()

        # Try direct parse
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to find a JSON object inside the text
            match = re.search(r"\{[\s\S]*\}", cleaned)
            if match:
                return json.loads(match.group())
            raise ValueError(f"Could not parse JSON from: {text[:200]}...")
