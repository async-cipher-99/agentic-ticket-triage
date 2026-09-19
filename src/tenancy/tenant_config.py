from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class EscalationConfig:
    min_confidence: float = 0.65
    max_agent_steps: int = 6


@dataclass
class RefundPolicy:
    max_auto_approve_amount_usd: Optional[float] = None
    requires_manager_review_above_usd: Optional[float] = None


@dataclass
class TenantConfig:
    tenant_id: str
    display_name: str
    supported_languages: List[str]
    allowed_tools: List[str]
    knowledge_base_path: str
    labels: List[str]
    urgency_levels: List[str]
    escalation: EscalationConfig
    refund_policy: Optional[RefundPolicy] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "TenantConfig":
        escalation = payload.get("escalation", {})
        refund = payload.get("refund_policy")
        return cls(
            tenant_id=str(payload["tenant_id"]),
            display_name=str(payload.get("display_name", payload["tenant_id"])),
            supported_languages=list(payload.get("supported_languages", ["en"])),
            allowed_tools=list(payload.get("allowed_tools", [])),
            knowledge_base_path=str(payload.get("knowledge_base_path", "")),
            labels=list(payload.get("labels", [])),
            urgency_levels=list(payload.get("urgency_levels", ["low", "medium", "high", "critical"])),
            escalation=EscalationConfig(
                min_confidence=float(escalation.get("min_confidence", 0.65)),
                max_agent_steps=int(escalation.get("max_agent_steps", 6)),
            ),
            refund_policy=(
                RefundPolicy(
                    max_auto_approve_amount_usd=refund.get("max_auto_approve_amount_usd"),
                    requires_manager_review_above_usd=refund.get("requires_manager_review_above_usd"),
                )
                if refund
                else None
            ),
        )


def load_tenant_config(path: str | Path) -> TenantConfig:
    with open(path, "r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    return TenantConfig.from_dict(payload)


def load_all_tenants(base_dir: str | Path) -> Dict[str, TenantConfig]:
    configs: Dict[str, TenantConfig] = {}
    for path in Path(base_dir).glob("*.yaml"):
        config = load_tenant_config(path)
        configs[config.tenant_id] = config
    return configs
