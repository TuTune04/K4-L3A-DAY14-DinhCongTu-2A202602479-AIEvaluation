"""Verify the completed lab's submitted files and benchmark evidence."""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
ANSWER_PROMPT = re.compile(
    r"^\s*>\s*\*(?:Câu trả lời|Điền|Paste output|Phân tích|Giải thích):\*(.*)$"
)


@pytest.mark.parametrize("filename", ["template.py", "solution/solution.py"])
def test_evaluation_core_is_complete(filename: str) -> None:
    assert "NotImplementedError" not in (ROOT / filename).read_text(encoding="utf-8")


def test_solution_matches_template() -> None:
    assert (ROOT / "template.py").read_bytes() == (ROOT / "solution/solution.py").read_bytes()


@pytest.mark.parametrize("filename", ["exercises.md", "reflection.md"])
def test_worksheet_answers_are_filled(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    assert "____" not in text
    assert "[paste Markdown table here]" not in text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = ANSWER_PROMPT.match(line)
        if match is None or match.group(1).strip():
            continue
        answer = next((item.strip() for item in lines[index + 1:] if item.strip()), "")
        assert answer and not answer.startswith("#"), (
            f"{filename}:{index + 1}: unanswered prompt"
        )


def test_env_is_not_tracked() -> None:
    if shutil.which("git") is None:
        pytest.skip("git is unavailable")
    result = subprocess.run(
        ["git", "ls-files", ".env"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    assert not result.stdout.strip(), ".env must not be tracked"


def test_benchmark_has_twenty_results() -> None:
    artifact = json.loads(
        (ROOT / "artifacts/benchmark_results.json").read_text(encoding="utf-8")
    )
    assert isinstance(artifact["results"], list)
    assert len(artifact["results"]) == 20


def test_completion_checklist_is_checked() -> None:
    text = (ROOT / "exercises.md").read_text(encoding="utf-8")
    checklist = text.split("## Completion Checklist", 1)[1]
    items = re.findall(r"^- \[([ xX])\] .+$", checklist, re.MULTILINE)
    assert items and all(item.lower() == "x" for item in items)
    assert "3.4" in checklist and "3.5" in checklist
