"""Exercise extractive generation without making API calls."""

from pathlib import Path

from domain_assistant import generate_actual_answers
from offline_generator import FALLBACK, ExtractiveGenerator


ROOT = Path(__file__).resolve().parents[1]


def test_generate_returns_context_sentences_in_overlap_order() -> None:
    prompt = """Question:
What is the laptop warranty repair policy?

Retrieved contexts:
[Context 1 | shipping.md]
Shipping takes two days. Laptop warranty lasts one year.

[Context 2 | warranty.md]
Laptop warranty repair requires a receipt. Repair requires approval.

Answer:"""
    answer = ExtractiveGenerator().generate(prompt)
    assert answer == (
        "Laptop warranty repair requires a receipt. "
        "Laptop warranty lasts one year. Repair requires approval."
    )


def test_generate_without_context_returns_fallback() -> None:
    prompt = """Question:
What is the warranty?

Retrieved contexts:
[No relevant context was retrieved.]

Answer:"""
    assert ExtractiveGenerator().generate(prompt) == FALLBACK


def test_generate_without_overlap_returns_fallback() -> None:
    prompt = """Question:
What is the warranty?

Retrieved contexts:
[Context 1 | shipping.md]
Shipping takes two days.

Answer:"""
    assert ExtractiveGenerator().generate(prompt) == FALLBACK


def test_generate_actual_answers_on_real_dataset() -> None:
    artifact = generate_actual_answers(
        ROOT / "golden_dataset.json",
        ROOT / "data/technology_store",
        generator=ExtractiveGenerator(),
        top_k=5,
    )
    assert artifact["agent"]["model"] == "offline-extractive-v1"
    assert len(artifact["answers"]) == 20
    for answer in artifact["answers"]:
        assert answer["actual_answer"].strip()
        assert len(answer["retrieved_contexts"]) == 5
        assert answer["error"] is None
