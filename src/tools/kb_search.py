from __future__ import annotations

from typing import Any, Dict, List


def kb_search(query: str, tenant_id: str, limit: int = 5) -> Dict[str, Any]:
    q = str(query).lower()
    candidates = {
        "acme_corp": {
            "billing": ["Refunds are reviewed within 3 to 5 business days.", "Duplicate charges are usually reversed after verification.", "Monthly invoices can be disputed if they contain incorrect amounts."],
            "shipping": ["Tracking updates may lag by 24 hours during carrier delays.", "Late deliveries are monitored through the order tracker.", "Packages can be rescheduled if the carrier marks them as delayed."],
            "technical_issue": ["App crashes are often caused by outdated versions.", "Export failures are tracked and typically fixed in the next patch release.", "Account lockouts can be resolved by resetting your password from the login screen."],
            "account_access": ["Too many failed login attempts trigger a temporary lockout.", "Security checks are triggered after repeated unsuccessful sign-ins.", "Password resets are required if a session is blocked by suspicious activity."],
            "feature_request": ["Bulk export requests are collected for roadmap review.", "CSV export improvements are often prioritized for power users.", "Feature requests may be grouped into weekly product planning cycles."],
        },
        "globex_manufacturing": {
            "technical_issue": ["High ambient heat can trigger thermal fault warnings.", "Production faults should be reviewed with the equipment serial number.", "Drive motor failures may require warranty review if they occur within the support window."],
            "warranty_claim": ["Warranty claims require service dates and model identifier.", "Failure reports are reviewed against maintenance history.", "Certification and service records are required for warranty evaluation."],
            "parts_order": ["Critical spare parts are prioritized for production shutdown scenarios.", "Exact part numbers are required before dispatch."],
            "installation_support": ["Intake-side clearance must be maintained to avoid airflow restrictions.", "Installation spacing is reviewed against machine specification manuals."],
            "compliance_question": ["CE proof and compliance paperwork are stored in the compliance archive.", "Audit requests are usually answered with the latest certification packet."],
        },
    }

    tenant_map = candidates.get(tenant_id, {})
    matches: List[str] = []
    for bucket, docs in tenant_map.items():
        if any(term in q for term in bucket.replace("_", " ").split()):
            matches.extend(docs)
        elif any(term in q for term in ["refund", "order", "login", "fault", "audit", "installation", "export", "shipping", "warranty", "part", "compliance"]):
            for doc in docs:
                if any(term in doc.lower() for term in q.split()):
                    matches.append(doc)

    if not matches:
        matches = ["Knowledge base does not contain a direct match, so the case should be escalated for manual review."]

    return {"tenant_id": tenant_id, "query": query, "results": matches[:limit]}
