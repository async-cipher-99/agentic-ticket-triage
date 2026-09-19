from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Ticket:
    ticket_id: str
    tenant_id: str
    language: str
    text: str
    gold_labels: List[str] = field(default_factory=list)
    gold_urgency: Optional[str] = None
    gold_tool_trace: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "tenant_id": self.tenant_id,
            "language": self.language,
            "text": self.text,
            "gold_labels": self.gold_labels,
            "gold_urgency": self.gold_urgency,
            "gold_tool_trace": self.gold_tool_trace,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Ticket":
        return cls(
            ticket_id=str(payload.get("ticket_id", "")),
            tenant_id=str(payload.get("tenant_id", "")),
            language=str(payload.get("language", "en")),
            text=str(payload.get("text", "")),
            gold_labels=list(payload.get("gold_labels", []) or []),
            gold_urgency=payload.get("gold_urgency"),
            gold_tool_trace=list(payload.get("gold_tool_trace", []) or []),
        )
