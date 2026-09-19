from src.agent.orchestrator import TicketOrchestrator
from src.classification.multilabel_classifier import TicketClassifier
from src.schema.ticket_schema import Ticket
from src.tenancy.tenant_config import load_tenant_config


def test_ticket_schema_round_trip():
    ticket = Ticket(
        ticket_id="T-1000",
        tenant_id="acme_corp",
        language="en",
        text="I need a refund for my damaged order and I may cancel.",
        gold_labels=["billing", "churn_risk"],
        gold_urgency="medium",
        gold_tool_trace=["order_status", "refund_lookup"],
    )
    assert ticket.ticket_id == "T-1000"
    assert ticket.gold_urgency == "medium"
    assert "billing" in ticket.gold_labels


def test_tenant_config_loads():
    config = load_tenant_config("configs/tenants/acme_corp.yaml")
    assert config.tenant_id == "acme_corp"
    assert "billing" in config.labels
    assert "order_status" in config.allowed_tools


def test_classifier_predicts_labels_from_keywords():
    classifier = TicketClassifier()
    result = classifier.predict("Refund request for damaged order and account access problem", "acme_corp")
    assert "billing" in result["labels"] or "account_access" in result["labels"]
    assert result["confidence"] >= 0.1


def test_orchestrator_returns_supported_result():
    orchestrator = TicketOrchestrator()
    ticket = Ticket(
        ticket_id="T-7777",
        tenant_id="globex_manufacturing",
        language="en",
        text="Our GX-4100 overheated while the production line was running and we need a fix right away.",
    )
    result = orchestrator.process_ticket(ticket)
    assert result["tenant_id"] == "globex_manufacturing"
    assert "technical_issue" in result["labels"]
    assert result["urgency"] in {"low", "medium", "high", "critical"}
    assert isinstance(result["tools"], list)
