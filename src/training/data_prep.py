from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def prepare_training_rows(source_path: str | Path, output_path: str | Path) -> List[Dict[str, str]]:
    source = Path(source_path)
    output = Path(output_path)
    rows: List[Dict[str, str]] = []
    with open(source, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            rows.append({
                "text": payload["text"],
                "labels": ", ".join(payload.get("gold_labels", [])),
                "urgency": payload.get("gold_urgency", "medium"),
            })

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    return rows
