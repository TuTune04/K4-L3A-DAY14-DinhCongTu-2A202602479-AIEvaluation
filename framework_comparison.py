"""Offline metric-definition comparison; does not run RAGAS or DeepEval.

Sentence support is lexical coverage >= 50%, not semantic entailment.
RAGAS has no intrinsic pass gate here: comparison_passed is a separate,
explicit 0.5 diagnostic gate used only to compare case decisions.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from evaluate_answers import load_evaluation_inputs
from template import QAPair, RAGASEvaluator, STOPWORDS

METRICS = ("faithfulness", "answer_relevancy", "context_recall")


def _tokens(text: str) -> set[str]:
    """Return unique lowercase content words using the lab's stopword list."""
    return set(re.findall(r"\b\w+\b", text.lower())) - STOPWORDS


def _sentence_support(text: str, evidence: set[str]) -> float:
    """Fraction of content-bearing sentences at least half supported.

    Split at terminal punctuation followed by whitespace/end, or newlines;
    decimal points remain intact. Empty/content-free text scores zero.
    """
    sentences = [_tokens(s) for s in re.split(r"[.!?]+(?:\s+|$)|\n+", text)]
    sentences = [tokens for tokens in sentences if tokens]
    if not sentences:
        return 0.0
    return sum(len(tokens & evidence) / len(tokens) >= 0.5
               for tokens in sentences) / len(sentences)


def ragas_style(question: str, answer: str, contexts: list[str],
                expected: str) -> dict[str, float]:
    """Return continuous offline proxies without applying a pass threshold.

    Relevancy is unique question-token coverage by the answer; an empty
    content-token question scores zero. Recall uses expected sentences.
    """
    evidence = _tokens("\n".join(contexts))
    question_tokens = _tokens(question)
    return {
        "faithfulness": _sentence_support(answer, evidence),
        "answer_relevancy": (len(_tokens(answer) & question_tokens)
                             / len(question_tokens) if question_tokens else 0.0),
        "context_recall": _sentence_support(expected, evidence),
    }


def deepeval_style(question: str, answer: str, contexts: list[str],
                   expected: str, threshold: float = 0.5,
                   strict_mode: bool = False) -> dict[str, Any]:
    """Apply DeepEval-like assertions to the same offline proxy definitions.

    Strict mode replaces scores below 1 with zero and forces threshold 1.
    A case passes only when every metric passes.
    """
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be in [0, 1]")
    raw = ragas_style(question, answer, contexts, expected)
    scores = {metric: float(score == 1.0) if strict_mode else score
              for metric, score in raw.items()}
    effective_threshold = 1.0 if strict_mode else threshold
    flags = {metric: score >= effective_threshold for metric, score in scores.items()}
    return {"raw_scores": raw, "scores": scores, "metric_passed": flags,
            "passed": all(flags.values()), "threshold": effective_threshold,
            "strict_mode": strict_mode}


def compare_frameworks(pairs: list[QAPair],
                       answers: dict[str, str]) -> dict[str, Any]:
    """Score identical saved inputs, including the unchanged lab reference."""
    evaluator = RAGASEvaluator()
    results: list[dict[str, Any]] = []
    for pair in pairs:
        answer = answers[pair.question]
        contexts = pair.retrieved_contexts or []
        inputs = (pair.question, answer, contexts, pair.expected_answer)
        scores = ragas_style(*inputs)
        core = evaluator.run_full_eval(answer, pair.question, "\n\n".join(contexts),
                                       pair.expected_answer, contexts)
        results.append({
            "id": pair.metadata["id"],
            "ragas_style": {"scores": scores,
                            "comparison_passed": all(s >= 0.5 for s in scores.values())},
            "deepeval_style": deepeval_style(*inputs),
            "deepeval_strict": deepeval_style(*inputs, strict_mode=True),
            "lab_core": {"passed": core.passed, "scores": {
                "faithfulness": core.faithfulness, "relevance": core.relevance,
                "completeness": core.completeness, "context_recall": core.context_recall,
                "context_precision": core.context_precision}},
        })
    count = len(results)
    summary: dict[str, Any] = {"case_count": count, "means": {},
                               "pass_rates": {}, "failed_ids": {}, "agreement_rate": {}}
    for name in ("ragas_style", "deepeval_style", "deepeval_strict", "lab_core"):
        flag = "comparison_passed" if name == "ragas_style" else "passed"
        metric_names = results[0][name]["scores"] if results else METRICS
        summary["means"][name] = {
            metric: sum(row[name]["scores"][metric] for row in results) / count
            if count else 0.0 for metric in metric_names}
        summary["failed_ids"][name] = [row["id"] for row in results if not row[name][flag]]
        summary["pass_rates"][name] = (sum(row[name][flag] for row in results) / count
                                             if count else 0.0)
    for name in ("deepeval_style", "deepeval_strict"):
        summary["agreement_rate"][name] = (sum(
            row["ragas_style"]["comparison_passed"] == row[name]["passed"]
            for row in results) / count if count else 0.0)
    return {
        "method": "offline lexical re-implementations; official packages not executed",
        "comparison_gate": {"threshold": 0.5, "rule": "all three metrics pass",
                            "note": "diagnostic only; RAGAS scores have no pass threshold"},
        "definitions": {"sentence_support": "content-token coverage >= 0.5",
                        "answer_relevancy": "answer/question overlap divided by question tokens",
                        "empty_text": "content-free sentences ignored; empty inputs score zero",
                        "strict_mode": "scores < 1 become 0; threshold becomes 1"},
        "sources": ["https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/",
                    "https://deepeval.com/docs/metrics-introduction",
                    "https://deepeval.com/docs/metrics-faithfulness"],
        "results": results, "summary": summary,
    }


def main() -> int:
    """Write deterministic full-precision results for the saved dataset."""
    root = Path(__file__).resolve().parent
    pairs, answers = load_evaluation_inputs(root / "golden_dataset.json",
                                            root / "artifacts/actual_answers.json")
    artifact = compare_frameworks(pairs, answers)
    output = root / "artifacts/framework_comparison.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(artifact["method"])
    summary = artifact["summary"]
    print(f"Cases: {summary['case_count']}")
    for name, means in summary["means"].items():
        formatted = ", ".join(f"{metric}={value:.3f}" for metric, value in means.items())
        print(f"{name}: {formatted}; pass={summary['pass_rates'][name]:.1%}")
    for name, rate in summary["agreement_rate"].items():
        print(f"Diagnostic RAGAS gate agreement with {name}: {rate:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
