"""Measure question-based reranking on the saved retrieval results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evaluate_answers import load_evaluation_inputs
from template import RAGASEvaluator, rerank_by_overlap


def compare_rerank(
    cases: list[tuple[str, str, str, list[str]]],
) -> list[dict[str, Any]]:
    """Return before/after retrieval scores without modifying input cases.

    Each tuple contains ID, question, expected answer, and retrieved texts.
    Only the question is supplied to the reranker; gold is used for scoring.
    """
    evaluator = RAGASEvaluator()
    results: list[dict[str, Any]] = []
    for case_id, question, expected, contexts in cases:
        reranked = rerank_by_overlap(contexts, question)
        before = {
            "context_recall": evaluator.evaluate_context_recall(contexts, expected),
            "context_precision": evaluator.evaluate_context_precision(contexts, expected),
        }
        after = {
            "context_recall": evaluator.evaluate_context_recall(reranked, expected),
            "context_precision": evaluator.evaluate_context_precision(reranked, expected),
        }
        results.append({
            "id": case_id,
            "before": before,
            "after": after,
            "delta": {metric: after[metric] - before[metric] for metric in before},
        })
    return results


def average_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute macro averages over all cases (zero for an empty input)."""
    return {
        "id": "Avg",
        **{
            stage: {
                metric: sum(row[stage][metric] for row in results) / len(results)
                if results else 0.0
                for metric in ("context_recall", "context_precision")
            }
            for stage in ("before", "after", "delta")
        },
    }


def markdown_table(results: list[dict[str, Any]]) -> str:
    """Render cases followed by their macro average at three decimals."""
    lines = [
        "| ID | Recall before | Recall after | Precision before | Precision after | Delta Precision |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in [*results, average_results(results)]:
        values = [row["before"]["context_recall"], row["after"]["context_recall"],
                  row["before"]["context_precision"], row["after"]["context_precision"],
                  row["delta"]["context_precision"]]
        lines.append(f"| {row['id']} | " + " | ".join(f"{value:.3f}" for value in values) + " |")
    return "\n".join(lines)


def main() -> int:
    """Join saved cases by ID, write full-precision scores, and print a table."""
    root = Path(__file__).resolve().parent
    pairs, _ = load_evaluation_inputs(
        root / "golden_dataset.json", root / "artifacts/actual_answers.json",
    )
    cases = [
        (pair.metadata["id"], pair.question, pair.expected_answer,
         pair.retrieved_contexts if pair.retrieved_contexts is not None else [])
        for pair in pairs
    ]
    results = compare_rerank(cases)
    output = root / "artifacts/rerank_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "reranker": "question_token_overlap",
        "results": results,
        "average": average_results(results),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(markdown_table(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
