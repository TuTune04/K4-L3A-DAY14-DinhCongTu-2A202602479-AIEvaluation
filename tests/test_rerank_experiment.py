"""Check reranking invariants and question-only ranking on real and toy cases."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from evaluate_answers import load_evaluation_inputs
from rerank_experiment import compare_rerank
from template import rerank_by_overlap


@pytest.mark.parametrize("contexts,query", [
    ([], "charger"),
    (["noise", "charger power", "noise", "charger adapter"], "charger"),
    (["one", "two", "one"], ""),
])
def test_rerank_preserves_chunks_and_stable_ties(contexts: list[str], query: str) -> None:
    original = contexts.copy()
    result = rerank_by_overlap(contexts, query)
    assert Counter(result) == Counter(original)
    assert contexts == original
    assert result is not contexts
    if query == "charger" and contexts:
        assert result == ["charger power", "charger adapter", "noise", "noise"]
    else:
        assert result == original


def test_relevant_chunk_moves_before_noise() -> None:
    contexts = ["garden flowers", "charger power adapter"]
    row = compare_rerank([("toy", "charger", "power adapter", contexts)])[0]
    assert row["before"]["context_precision"] == 0.5
    assert row["after"]["context_precision"] == 1.0
    assert row["delta"]["context_precision"] == 0.5
    assert row["before"]["context_recall"] == row["after"]["context_recall"]
    assert contexts == ["garden flowers", "charger power adapter"]


def test_ranking_uses_question_instead_of_gold() -> None:
    row = compare_rerank([
        ("toy", "flowers", "adapter", ["adapter", "flowers"]),
    ])[0]
    assert row["before"]["context_precision"] == 1.0
    assert row["after"]["context_precision"] == 0.5


def test_recall_is_unchanged_for_every_saved_case() -> None:
    root = Path(__file__).resolve().parents[1]
    pairs, _ = load_evaluation_inputs(
        root / "golden_dataset.json", root / "artifacts/actual_answers.json",
    )
    cases = [(pair.metadata["id"], pair.question, pair.expected_answer,
              pair.retrieved_contexts or []) for pair in pairs]
    rows = compare_rerank(cases)
    assert len(rows) == len(pairs) == 20
    for row, (_, question, _, contexts) in zip(rows, cases):
        assert row["before"]["context_recall"] == row["after"]["context_recall"]
        assert row["delta"]["context_recall"] == 0.0
        assert Counter(rerank_by_overlap(contexts, question)) == Counter(contexts)
