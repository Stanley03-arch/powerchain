from __future__ import annotations

from typing import Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.eval.evaluator import Evaluator, EvalResult


class QAEvaluator(Evaluator):
    """LLM-as-judge evaluator for question-answering.

    Asks the model to score how well the prediction answers the question
    given the reference (if available).
    """

    def __init__(self, llm: BaseChatModel, pass_threshold: float = 0.7):
        self.llm = llm
        self.pass_threshold = pass_threshold

    def evaluate(self, input: str, prediction: str, reference: Optional[str] = None) -> EvalResult:
        if reference:
            prompt = (
                "You are an evaluation judge. Score how well the PREDICTION answers the QUESTION "
                "compared to the REFERENCE answer.\n\n"
                f"QUESTION: {input}\n\n"
                f"REFERENCE: {reference}\n\n"
                f"PREDICTION: {prediction}\n\n"
                "Reply with ONLY a number between 0 and 1 (e.g. 0.85)."
            )
        else:
            prompt = (
                "You are an evaluation judge. Score how helpful and correct the PREDICTION is "
                "for the given QUESTION.\n\n"
                f"QUESTION: {input}\n\n"
                f"PREDICTION: {prediction}\n\n"
                "Reply with ONLY a number between 0 and 1 (e.g. 0.85)."
            )

        response = self.llm.invoke([ChatMessage(role=Role.USER, content=prompt)])
        raw = response.content.strip()

        try:
            # Extract first floating point number found
            import re
            match = re.search(r"0?\.\d+|1\.0|1|0", raw)
            score = float(match.group()) if match else 0.0
            score = max(0.0, min(1.0, score))
        except Exception:
            score = 0.0

        return EvalResult(
            input=input,
            prediction=prediction,
            reference=reference,
            score=score,
            passed=score >= self.pass_threshold,
            metadata={"raw_judge_output": raw},
        )
