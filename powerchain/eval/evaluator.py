from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EvalResult:
    """Result of a single evaluation example."""

    input: str
    prediction: str
    reference: Optional[str] = None
    score: float = 0.0
    passed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"EvalResult({status}, score={self.score:.2f})"


class Evaluator(ABC):
    """Base evaluator interface."""

    @abstractmethod
    def evaluate(self, input: str, prediction: str, reference: Optional[str] = None) -> EvalResult:
        ...

    def evaluate_batch(
        self,
        inputs: List[str],
        predictions: List[str],
        references: Optional[List[str]] = None,
    ) -> List[EvalResult]:
        refs = references or [None] * len(inputs)
        return [
            self.evaluate(inp, pred, ref)
            for inp, pred, ref in zip(inputs, predictions, refs)
        ]

    def summary(self, results: List[EvalResult]) -> Dict[str, Any]:
        if not results:
            return {"count": 0, "pass_rate": 0.0, "avg_score": 0.0}

        passed = sum(1 for r in results if r.passed)
        avg_score = sum(r.score for r in results) / len(results)
        return {
            "count": len(results),
            "passed": passed,
            "pass_rate": passed / len(results),
            "avg_score": avg_score,
        }
