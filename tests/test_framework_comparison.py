"""Check offline metric definitions and saved comparison reproducibility."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from evaluate_answers import load_evaluation_inputs
from framework_comparison import compare_frameworks, deepeval_style, ragas_style

ROOT = Path(__file__).resolve().parents[1]


def test_sentence_support_and_recall() -> None:
    scores = ragas_style("battery warranty", "Battery warranty lasts years. Aliens dance.",
                         ["Battery warranty lasts years."], "Battery warranty. Aliens dance.")
    assert scores == {"faithfulness": 0.5, "answer_relevancy": 1.0, "context_recall": 0.5}
    assert ragas_style("battery", "Battery warranty lasts years.",
                       ["Battery warranty lasts years."], "Battery warranty.")["faithfulness"] == 1.0


def test_unsupported_answer_fails() -> None:
    result = deepeval_style("battery", "Aliens dance.", ["Battery warranty."], "Battery warranty.")
    assert result["scores"]["faithfulness"] == 0.0
    assert not result["passed"]


def test_threshold_boundary_and_strict_rounding() -> None:
    inputs = ("battery warranty", "Battery lasts years.", ["Battery lasts years."], "Battery lasts years.")
    normal = deepeval_style(*inputs)
    strict = deepeval_style(*inputs, strict_mode=True)
    assert normal["scores"]["answer_relevancy"] == 0.5
    assert normal["passed"]
    assert strict["scores"]["answer_relevancy"] == 0.0
    assert not strict["passed"]
    assert deepeval_style("battery", "Battery.", ["Battery."], "Battery.", strict_mode=True)["passed"]


@pytest.mark.parametrize("threshold", [-0.1, 1.1])
def test_invalid_threshold(threshold: float) -> None:
    with pytest.raises(ValueError):
        deepeval_style("", "", [], "", threshold=threshold)


def test_empty_inputs_and_decimal_sentences() -> None:
    assert all(score == 0.0 for score in ragas_style("", "", [], "").values())
    scores = ragas_style("fee", "Fee 1.5 dollars. Aliens dance.",
                         ["Fee 1.5 dollars."], "Fee 1.5 dollars.")
    assert scores["faithfulness"] == 0.5
    assert scores["context_recall"] == 1.0


def test_dataset_scores_summary_and_artifact() -> None:
    pairs, answers = load_evaluation_inputs(ROOT / "golden_dataset.json",
                                            ROOT / "artifacts/actual_answers.json")
    artifact = compare_frameworks(pairs, answers)
    assert len(artifact["results"]) == 20
    assert artifact == json.loads((ROOT / "artifacts/framework_comparison.json").read_text())
    summary = artifact["summary"]
    assert {"means", "pass_rates", "agreement_rate", "failed_ids", "case_count"} <= summary.keys()
    for row in artifact["results"]:
        for framework in ("ragas_style", "deepeval_style", "deepeval_strict", "lab_core"):
            assert all(0 <= value <= 1 for value in row[framework]["scores"].values())
        assert row["ragas_style"]["scores"] == row["deepeval_style"]["raw_scores"]
        assert not row["deepeval_strict"]["passed"] or row["deepeval_style"]["passed"]
    assert summary["agreement_rate"]["deepeval_style"] == 1.0
    assert compare_frameworks([], {})["summary"]["case_count"] == 0
