"""Deterministic extractive generator for API-free tests and local experiments."""

from __future__ import annotations

import json
import re
from pathlib import Path

from domain_assistant import _tokenize, generate_actual_answers


FALLBACK = (
    "The retrieved OrbitTech documents do not contain enough evidence to answer "
    "this; please contact OrbitTech support."
)


class ExtractiveGenerator:
    """Return up to three context sentences ranked by question token overlap."""

    model = "offline-extractive-v1"

    def generate(self, prompt: str) -> str:
        """Extract evidence from the format emitted by domain_assistant._build_prompt."""
        match = re.search(
            r"Question:\s*\n(.*?)\n\s*Retrieved contexts:\s*\n(.*)",
            prompt,
            re.DOTALL,
        )
        if match is None:
            return FALLBACK
        question_tokens = set(_tokenize(match.group(1)))
        context_section = re.sub(r"\n\s*Answer:\s*$", "", match.group(2))
        bodies = re.split(
            r"(?m)^\[Context \d+ \| [^\n]+\]\s*\n", context_section
        )[1:]
        scored: list[tuple[int, str]] = []
        for body in bodies:
            for sentence in re.split(r"(?<=[.!?])\s+|\n+", body.strip()):
                sentence = sentence.strip()
                score = len(question_tokens.intersection(_tokenize(sentence)))
                if score > 0:
                    scored.append((score, sentence))
        scored.sort(key=lambda item: -item[0])
        return " ".join(sentence for _, sentence in scored[:3]) or FALLBACK


def main() -> int:
    """Write a separate offline artifact, preserving the submitted real answers."""
    artifact = generate_actual_answers(
        "golden_dataset.json",
        "data/technology_store",
        generator=ExtractiveGenerator(),
        top_k=5,
        progress=print,
    )
    output = Path("artifacts/actual_answers_offline.json").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(artifact['answers'])} actual answers: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
