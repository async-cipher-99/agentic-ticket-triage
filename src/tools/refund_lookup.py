from __future__ import annotations

from typing import Any, Dict


def refund_lookup(order_id: str, amount: float | None = None, tenant_id: str = "acme_corp") -> Dict[str, Any]:
    order = str(order_id).upper()
    refund_amount = float(amount) if amount is not None else 129.0
    return {
        "tenant_id": tenant_id,
        "order_id": order,
        "status": "under_review",
        "refund_amount_usd": round(refund_amount, 2),
        "decision": "manual_review_required",
        "notes": "The refund is under review because the condition is outside the auto-approval threshold.",
    }
