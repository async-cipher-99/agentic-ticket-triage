from src.schema.ticket_schema import Ticket


def test_ticket_to_dict_round_trip():
    ticket = Ticket(
        ticket_id="T-100",
        tenant_id="acme_corp",
        language="en",
        text="I need a refund for my damaged order.",
        gold_labels=["billing"],
        gold_urgency="medium",
        gold_tool_trace=["refund_lookup"],
    )
    payload = ticket.to_dict()
    assert payload["ticket_id"] == "T-100"
    assert payload["gold_labels"] == ["billing"]

    rebuilt = Ticket.from_dict(payload)
    assert rebuilt.ticket_id == ticket.ticket_id
    assert rebuilt.language == "en"
