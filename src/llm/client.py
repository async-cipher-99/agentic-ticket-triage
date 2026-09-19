from __future__ import annotations

from typing import Dict, Optional


class LLMClient:
    def __init__(self, model_name: str = "local") -> None:
        self.model_name = model_name

    def generate(self, prompt: str, **kwargs) -> str:
        return f"[{self.model_name}] {prompt[:200]}"

    def classify(self, text: str, tenant_id: str, label_space: Optional[list[str]] = None) -> Dict[str, object]:
        if label_space is None:
            label_space = ["billing", "shipping", "technical_issue", "account_access", "churn_risk", "feature_request"]
        return {"labels": label_space[:2], "confidence": 0.7}
