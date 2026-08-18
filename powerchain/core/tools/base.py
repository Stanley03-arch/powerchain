from __future__ import annotations

import inspect
import json
from typing import Any, Callable, Dict, List, Optional, get_type_hints

from pydantic import BaseModel, Field, create_model


class BaseTool(BaseModel):
    name: str
    description: str
    args_schema: Optional[type[BaseModel]] = None

    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def arun(self, **kwargs: Any) -> Any:
        return self.run(**kwargs)

    def to_openai_tool(self) -> dict:
        """Convert to OpenAI function-calling format."""
        parameters: dict[str, Any] = {"type": "object", "properties": {}, "required": []}

        if self.args_schema:
            schema = self.args_schema.model_json_schema()
            parameters["properties"] = schema.get("properties", {})
            parameters["required"] = schema.get("required", [])

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters,
            },
        }


class Tool(BaseTool):
    """Concrete tool backed by a Python function."""

    func: Callable[..., Any] = Field(exclude=True)

    def run(self, **kwargs: Any) -> Any:
        return self.func(**kwargs)

    async def arun(self, **kwargs: Any) -> Any:
        result = self.func(**kwargs)
        if inspect.iscoroutine(result):
            return await result
        return result


def _create_args_schema(func: Callable) -> type[BaseModel]:
    hints = get_type_hints(func)
    hints.pop("return", None)
    fields: Dict[str, Any] = {}

    sig = inspect.signature(func)
    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        annotation = hints.get(name, Any)
        default = param.default if param.default is not inspect.Parameter.empty else ...
        fields[name] = (annotation, default)

    return create_model(f"{func.__name__}Args", **fields)


def tool(
    func: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Any:
    """Decorator to turn a function into a PowerChain Tool."""

    def decorator(fn: Callable) -> Tool:
        tool_name = name or fn.__name__
        tool_description = description or (fn.__doc__ or "").strip() or f"Tool: {tool_name}"
        schema = _create_args_schema(fn)

        return Tool(
            name=tool_name,
            description=tool_description,
            args_schema=schema,
            func=fn,
        )

    if func is not None:
        return decorator(func)
    return decorator
