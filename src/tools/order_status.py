from __future__ import annotations

from typing import Any, Dict


def order_status(order_id: str, tenant_id: str) -> Dict[str, Any]:
    normalized = str(order_id).upper()
    stage = "in_transit" if "A" in normalized or "TRK" in normalized else "processing"
    return {
        "tenant_id": tenant_id,
        "order_id": normalized,
        "status": stage,
        "estimated_delivery": "3-5 business days",
        "carrier": "priority shipping",
        "notes": "Tracking has been updated and the shipment remains within the expected delivery window.",
    }
