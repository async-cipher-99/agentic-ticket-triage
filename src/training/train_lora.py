from __future__ import annotations

from pathlib import Path
from typing import Any


def build_training_plan(config_path: str | Path) -> dict[str, Any]:
    return {
        "config": str(config_path),
        "status": "ready",
        "target": "Qwen/Qwen2.5-1.5B-Instruct",
    }
