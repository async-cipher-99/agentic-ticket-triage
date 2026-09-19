from __future__ import annotations

from typing import Iterable, List


def accuracy_score(predictions: Iterable[bool]) -> float:
    items = list(predictions)
    if not items:
        return 0.0
    return sum(items) / len(items)


def micro_f1(labels: List[str], expected: List[str]) -> float:
    if not labels and not expected:
        return 1.0
    true_positive = len(set(labels) & set(expected))
    precision = true_positive / max(len(set(labels)), 1)
    recall = true_positive / max(len(set(expected)), 1)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
