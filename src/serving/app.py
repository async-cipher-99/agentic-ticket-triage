from __future__ import annotations

from fastapi import FastAPI

from src.agent.orchestrator import TicketOrchestrator
from src.schema.ticket_schema import Ticket

app = FastAPI(title="Ticket Triage Agent")
app.state.orchestrator = TicketOrchestrator()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tickets/process")
def process_ticket(payload: dict) -> dict:
    ticket = Ticket.from_dict(payload)
    result = app.state.orchestrator.process_ticket(ticket)
    return result
