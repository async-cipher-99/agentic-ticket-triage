from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def build_qlora_config(config_path: str | Path) -> Dict[str, Any]:
    return {
        "config_path": str(config_path),
        "quantization": "4bit",
        "target_model": "Qwen/Qwen2.5-1.5B-Instruct",
        "status": "configured",
    }
