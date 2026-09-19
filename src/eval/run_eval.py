from __future__ import annotations

from typing import Iterable, List

from src.eval.metrics import accuracy_score, micro_f1


def run_eval(prediction_scores: Iterable[bool], labels: List[str], expected: List[str]) -> dict:
    return {
        "accuracy": accuracy_score(prediction_scores),
        "micro_f1": micro_f1(labels, expected),
    }
