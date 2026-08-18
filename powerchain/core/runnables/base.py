from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Sequence


class Runnable(ABC):
    """Base class for composable units (inspired by but cleaner than LCEL)."""

    @abstractmethod
    def invoke(self, input: Any, **kwargs: Any) -> Any:
        ...

    async def ainvoke(self, input: Any, **kwargs: Any) -> Any:
        return self.invoke(input, **kwargs)

    def __or__(self, other: "Runnable") -> "Sequential":
        """Allow pipe-style composition: a | b | c"""
        return Sequential([self, other])

    def __repr__(self) -> str:
        return self.__class__.__name__


class Sequential(Runnable):
    """Run a sequence of runnables, passing output of one to the next."""

    def __init__(self, steps: Sequence[Runnable]):
        self.steps = list(steps)

    def invoke(self, input: Any, **kwargs: Any) -> Any:
        result = input
        for step in self.steps:
            result = step.invoke(result, **kwargs)
        return result

    async def ainvoke(self, input: Any, **kwargs: Any) -> Any:
        result = input
        for step in self.steps:
            result = await step.ainvoke(result, **kwargs)
        return result

    def __or__(self, other: Runnable) -> "Sequential":
        return Sequential(self.steps + [other])


class Parallel(Runnable):
    """Run multiple runnables in parallel on the same input and return a dict of results."""

    def __init__(self, steps: dict[str, Runnable]):
        self.steps = steps

    def invoke(self, input: Any, **kwargs: Any) -> dict[str, Any]:
        return {name: step.invoke(input, **kwargs) for name, step in self.steps.items()}

    async def ainvoke(self, input: Any, **kwargs: Any) -> dict[str, Any]:
        # Simple sequential for now; can be upgraded to true concurrency later
        results = {}
        for name, step in self.steps.items():
            results[name] = await step.ainvoke(input, **kwargs)
        return results


class FunctionRunnable(Runnable):
    """Wrap a plain function as a Runnable."""

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def invoke(self, input: Any, **kwargs: Any) -> Any:
        return self.func(input)
