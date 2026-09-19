from __future__ import annotations

from typing import Any, Dict


def account_lookup(account_id: str, tenant_id: str) -> Dict[str, Any]:
    account = str(account_id).upper()
    return {
        "tenant_id": tenant_id,
        "account_id": account,
        "status": "active",
        "service_history": "covered under maintenance plan",
        "risk_level": "medium",
        "notes": "Customer account is active, and service history indicates prior maintenance activity on the asset.",
    }
