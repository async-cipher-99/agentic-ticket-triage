from __future__ import annotations

from pathlib import Path
from typing import Dict, List


class VectorStore:
    def __init__(self, base_path: str | Path = "data/knowledge_base") -> None:
        self.base_path = Path(base_path)

    def load(self, tenant_id: str) -> List[Dict[str, str]]:
        file_path = self.base_path / f"{tenant_id}.jsonl"
        if not file_path.exists():
            return []
        items: List[Dict[str, str]] = []
        with open(file_path, "r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    items.append({"content": line.strip()})
        return items

    def search(self, tenant_id: str, query: str, limit: int = 5) -> List[str]:
        data = self.load(tenant_id)
        query_lower = query.lower()
        matches = []
        for item in data:
            content = item.get("content", "")
            if query_lower in content.lower():
                matches.append(content)
        return matches[:limit]
