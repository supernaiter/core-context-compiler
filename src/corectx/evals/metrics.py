from __future__ import annotations

import math
from collections.abc import Iterable

from corectx.schemas import EvalQuestion, EvalResult

TOKEN_COST_USD = 0.000002


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * pct) - 1))
    return ordered[index]


def abstention_f1(results: list[EvalResult], questions_by_id: dict[str, EvalQuestion]) -> float:
    tp = fp = fn = 0
    for result in results:
        expected = questions_by_id[result.qid].expected_behavior == "abstain"
        if result.abstained and expected:
            tp += 1
        elif result.abstained and not expected:
            fp += 1
        elif not result.abstained and expected:
            fn += 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def summarize_results(
    results: Iterable[EvalResult],
    questions: list[EvalQuestion],
) -> dict[str, dict[str, float]]:
    rows = list(results)
    questions_by_id = {question.qid: question for question in questions}
    baselines = sorted({row.baseline for row in rows})
    summary: dict[str, dict[str, float]] = {}
    for baseline in baselines:
        subset = [row for row in rows if row.baseline == baseline]
        correct = sum(1 for row in subset if row.correct)
        total_tokens = sum(row.input_tokens for row in subset)
        total_recall_tokens = sum(row.recall_tokens for row in subset)
        total_cost = sum(row.cost for row in subset)
        source_scores = [
            row.source_recall_at5
            for row in subset
            if questions_by_id[row.qid].required_sources
        ]
        summary[baseline] = {
            "answer_accuracy": mean([1.0 if row.correct else 0.0 for row in subset]),
            "source_recall@5": mean(source_scores),
            "stale_answer_rate": mean([1.0 if row.stale_answer else 0.0 for row in subset]),
            "abstention_f1": abstention_f1(subset, questions_by_id),
            "total_input_tokens": float(total_tokens),
            "total_recall_tokens": float(total_recall_tokens),
            "avg_latency_ms": mean([row.latency_ms for row in subset]),
            "latency_p95": percentile([row.latency_ms for row in subset], 0.95),
            "total_cost": total_cost,
            "cost_per_correct_answer": (
                float(total_cost / correct) if correct else float(total_cost)
            ),
        }
    return summary


def label_error(result: EvalResult, question: EvalQuestion) -> str | None:
    if result.correct:
        return None
    if result.stale_answer:
        return "stale_answer"
    if question.expected_behavior == "abstain" and not result.abstained:
        return "abstention_miss"
    if question.expected_behavior != "abstain" and result.abstained:
        return "false_abstention"
    if question.required_sources and result.source_recall_at5 < 1.0:
        return "source_miss"
    return "wrong_answer"


def estimate_cost(input_tokens: int, *, token_cost_usd: float = TOKEN_COST_USD) -> float:
    return input_tokens * token_cost_usd
