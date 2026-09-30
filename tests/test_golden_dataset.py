"""Check the submitted golden dataset against its corpus contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from validate_golden_dataset import build_contract, validate_dataset


def test_golden_dataset_contract() -> None:
    """Require valid evidence, fixed difficulty counts, and full coverage."""
    contract = build_contract(ROOT / "data" / "technology_store")
    dataset = json.loads((ROOT / "golden_dataset.json").read_text(encoding="utf-8"))
    errors, stats = validate_dataset(dataset, contract)

    assert errors == []
    assert len(dataset["qa_pairs"]) == stats["qa_count"] == 20
    assert stats["difficulty_counts"] == {
        "easy": 5,
        "medium": 7,
        "hard": 5,
        "adversarial": 3,
    }
    assert len(stats["used_documents"]) == 10
    assert stats["used_documents"] == set(contract.source_texts)
