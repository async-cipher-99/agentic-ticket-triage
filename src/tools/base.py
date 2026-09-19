from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ToolSpec:
    name: str
    description: str
    supported_labels: List[str] = field(default_factory=list)


def get_tool_registry() -> Dict[str, ToolSpec]:
    return {
        "order_status": ToolSpec("order_status", "Check order lifecycle and shipping status", ["shipping", "billing"]),
        "refund_lookup": ToolSpec("refund_lookup", "Look up refund or payment records", ["billing"]),
        "account_lookup": ToolSpec("account_lookup", "Lookup customer account and service history", ["account_access", "warranty_claim", "technical_issue"]),
        "kb_search": ToolSpec("kb_search", "Search product knowledge base and policies", ["technical_issue", "feature_request", "compliance_question", "installation_support"]),
    }


def choose_tools_for_labels(labels: List[str], allowed_tools: List[str]) -> List[str]:
    registry = get_tool_registry()
    selected: List[str] = []
    for name in allowed_tools:
        tool = registry.get(name)
        if tool and any(label in tool.supported_labels for label in labels):
            selected.append(name)
    return selected or allowed_tools[:1]
