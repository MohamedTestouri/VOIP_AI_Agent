from app.schemas import InvestigationRequest
from app.services.investigations import plan_investigation


def test_plan_is_explicitly_not_execution():
    request = InvestigationRequest(title="Investigate Kamailio SIP routing", description="A SIP INVITE receives a 404; inspect kamailio.cfg and call flow", kind="investigation")
    plan = plan_investigation(request)
    assert plan["status"] == "planned"
    assert plan["execution_mode"] == "deterministic-planner"
    assert "kamailio" in plan["selected_agents"]
    assert any("does not execute" in item for item in plan["limitations"])
