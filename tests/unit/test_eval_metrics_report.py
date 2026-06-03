from __future__ import annotations

from corectx.evals.metrics import estimate_cost, label_error, summarize_results
from corectx.evals.report import render_summary
from corectx.schemas import EvalQuestion, EvalResult


def _question(qid: str, *, expected_behavior: str = "answer") -> EvalQuestion:
    return EvalQuestion(
        qid=qid,
        question="q",
        expected_behavior=expected_behavior,
        expected_answer="yes" if expected_behavior == "answer" else None,
        required_sources=["s1"],
    )


def _result(**overrides) -> EvalResult:
    data = {
        "run_id": "r1",
        "baseline": "compressed_core",
        "qid": "q1",
        "answer": "yes",
        "abstained": False,
        "correct": True,
        "source_recall_at5": 1.0,
        "stale_answer": False,
        "input_tokens": 100,
        "recall_tokens": 12,
        "latency_ms": 2.5,
        "cost": estimate_cost(100),
    }
    data.update(overrides)
    return EvalResult(**data)


def test_summarize_results_includes_budget_cost_latency_metrics() -> None:
    metrics = summarize_results([_result(), _result(input_tokens=50, cost=0.1)], [_question("q1")])

    row = metrics["compressed_core"]
    assert row["total_input_tokens"] == 150
    assert row["total_recall_tokens"] == 24
    assert row["avg_latency_ms"] == 2.5
    assert row["total_cost"] == estimate_cost(100) + 0.1
    assert row["cost_per_correct_answer"] == (estimate_cost(100) + 0.1) / 2


def test_error_labels_are_specific() -> None:
    question = _question("q1")
    assert label_error(_result(correct=False, stale_answer=True), question) == "stale_answer"
    assert (
        label_error(_result(correct=False, abstained=True), question)
        == "false_abstention"
    )
    assert (
        label_error(_result(correct=False, source_recall_at5=0.0), question)
        == "source_miss"
    )
    assert (
        label_error(
            _result(correct=False, abstained=False),
            _question("q1", expected_behavior="abstain"),
        )
        == "abstention_miss"
    )


def test_render_summary_has_comparison_table() -> None:
    markdown = render_summary(
        {
            "compressed_core": {
                "answer_accuracy": 1.0,
                "source_recall@5": 0.5,
                "abstention_f1": 1.0,
                "total_input_tokens": 100.0,
                "total_recall_tokens": 10.0,
                "total_cost": 0.01,
                "avg_latency_ms": 3.0,
            }
        }
    )

    assert "## Comparison" in markdown
    assert (
        "| system | accuracy | source@5 | stale | abstention_f1 | input_tokens | latency_p95 |"
        in markdown
    )
    assert "| compressed_core | 1.0000 | 0.5000 |" in markdown
