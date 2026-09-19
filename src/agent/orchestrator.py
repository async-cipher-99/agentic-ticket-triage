from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.classification.multilabel_classifier import TicketClassifier
from src.schema.ticket_schema import Ticket
from src.tenancy.tenant_config import load_tenant_config


class TicketOrchestrator:
    def __init__(self, tenant_dir: str | Path = "configs/tenants") -> None:
        self.tenant_dir = Path(tenant_dir)
        self.classifier = TicketClassifier()

    def _resolve_tenant(self, tenant_id: str):
        return load_tenant_config(self.tenant_dir / f"{tenant_id}.yaml")

    def _urgency_from_text(self, text: str, labels: List[str], tenant_config) -> str:
        normalized = text.lower()
        urgency_order = tenant_config.urgency_levels
        if any(word in normalized for word in ["production line down", "urgent", "critical", "down", "outage", "line is down", "audit next week", "resolved fast"]):
            return "critical"
        if any(word in normalized for word in ["failed", "not working", "cannot access", "damaged", "stopped", "overheat", "refund", "cancel", "lockout", "server down"]):
            return "high"
        if any(word in normalized for word in ["needs", "request", "considering", "expensive", "issue", "error", "bulk export", "report", "weekly"]):
            return "medium"
        return "low"

    def _tool_plan(self, text: str, labels: List[str], tenant_config) -> List[str]:
        normalized = text.lower()
        tools: List[str] = []
        for tool in tenant_config.allowed_tools:
            if tool == "order_status" and any(word in normalized for word in ["order", "tracking", "shipment", "delivery", "package"]):
                tools.append(tool)
            if tool == "refund_lookup" and any(word in normalized for word in ["refund", "charged", "invoice", "payment", "money back"]):
                tools.append(tool)
            if tool == "account_lookup" and any(word in normalized for word in ["account", "serial", "customer number", "account number", "glx", "service history"]):
                tools.append(tool)
            if tool == "kb_search" and any(word in normalized for word in ["error", "faq", "document", "manual", "how to", "install", "compliance", "support", "issue", "specification"]):
                tools.append(tool)
        if not tools and tenant_config.allowed_tools:
            tools = [tenant_config.allowed_tools[0]]
        return tools

    def process_ticket(self, ticket: Ticket) -> Dict[str, Any]:
        tenant_config = self._resolve_tenant(ticket.tenant_id)
        classification = self.classifier.predict(ticket.text, ticket.tenant_id)
        urgency = self._urgency_from_text(ticket.text, classification["labels"], tenant_config)
        tools = self._tool_plan(ticket.text, classification["labels"], tenant_config)

        return {
            "ticket_id": ticket.ticket_id,
            "tenant_id": ticket.tenant_id,
            "language": ticket.language,
            "labels": classification["labels"],
            "confidence": classification["confidence"],
            "urgency": urgency,
            "tools": tools,
            "escalation_required": classification["confidence"] >= tenant_config.escalation.min_confidence and urgency in {"high", "critical"},
        }
