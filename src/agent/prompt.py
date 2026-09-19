from __future__ import annotations

from typing import Any, Dict, List


def build_ticket_prompt(ticket_text: str, tenant_id: str, label_space: List[str]) -> str:
    labels = ", ".join(label_space)
    return (
        f"You are triaging a support ticket for tenant {tenant_id}. "
        f"Ticket text: {ticket_text}. "
        f"Choose the most relevant labels from: {labels}."
    )


def build_agent_response(ticket_text: str, labels: List[str], urgency: str) -> Dict[str, Any]:
    return {
        "summary": ticket_text[:120],
        "labels": labels,
        "urgency": urgency,
    }
