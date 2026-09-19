from __future__ import annotations

from src.agent.orchestrator import TicketOrchestrator


def get_orchestrator() -> TicketOrchestrator:
    return TicketOrchestrator()
