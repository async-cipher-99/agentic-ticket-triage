from src.tenancy.tenant_config import load_tenant_config


def test_acme_tenant_config():
    config = load_tenant_config("configs/tenants/acme_corp.yaml")
    assert config.tenant_id == "acme_corp"
    assert "billing" in config.labels
    assert "order_status" in config.allowed_tools


def test_globex_tenant_config():
    config = load_tenant_config("configs/tenants/globex_manufacturing.yaml")
    assert config.tenant_id == "globex_manufacturing"
    assert "compliance_question" in config.labels
    assert config.escalation.min_confidence > 0.7
