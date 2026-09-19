from __future__ import annotations

from typing import Dict, List

from src.tenancy.tenant_config import load_tenant_config


class TicketClassifier:
    def __init__(self) -> None:
        self.label_keywords = {
            "billing": ["refund", "charged", "charge", "invoice", "payment", "billing", "double charged", "credit card", "amount", "money", "receipt", "charged twice", "payment issue"],
            "shipping": ["shipping", "delivery", "package", "tracking", "shipment", "order status", "lost parcel", "late delivery", "tracking number", "carrier"],
            "technical_issue": ["bug", "crash", "error", "fault", "not working", "issue", "failed", "malfunction", "overheat", "production line down", "application crash", "server down"],
            "account_access": ["login", "locked out", "password", "account", "access denied", "verification", "two factor", "cannot sign in", "session expired"],
            "churn_risk": ["cancel", "done with this product", "switching providers", "leave", "cancel service", "considering cancelling", "too expensive", "unsubscribe", "not worth it"],
            "feature_request": ["feature", "request", "add", "enhancement", "bulk export", "csv", "ability", "would like", "improvement"],
            "warranty_claim": ["warranty", "repair", "replacement", "coverage", "guarantee", "claim"],
            "parts_order": ["parts", "spare parts", "replacement motor", "order parts", "component", "part number"],
            "installation_support": ["installation", "setup", "install", "clearance", "mounting", "connection", "clearance requirement"],
            "compliance_question": ["compliance", "certification", "ce", "audit", "regulation", "documentation", "conformity", "iso"],
        }

    def predict(self, text: str, tenant_id: str) -> Dict[str, object]:
        normalized = text.lower()
        tenant_config = load_tenant_config(f"configs/tenants/{tenant_id}.yaml")
        labels: List[str] = []
        matches = 0

        for label, keywords in self.label_keywords.items():
            if label in tenant_config.labels:
                if any(keyword in normalized for keyword in keywords):
                    labels.append(label)
                    matches += 1

        if not labels:
            labels = [tenant_config.labels[0]] if tenant_config.labels else ["technical_issue"]

        confidence = min(0.99, max(0.35, 0.36 + (matches * 0.14)))
        return {"labels": labels, "confidence": round(confidence, 2)}
