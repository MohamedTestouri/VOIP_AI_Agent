"""Transparent, deterministic investigation planner; no pretend agent execution."""
from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any
from app.schemas import InvestigationRequest

ROLE_MAP = {
    "voip-protocol": ["sip", "rtp", "pcap", "call", "dnd", "blf", "forward", "codec", "registration"],
    "kamailio": ["kamailio", "route", "cfg", "routing"],
    "saylo-architect": ["saylo", "api", "database", "provision", "rabbitmq", "hangfire", "redis", ".net", "angular"],
    "feature-engineer": ["feature", "implement", "add", "support"],
    "quality-performance": ["refactor", "optimize", "performance", "duplicate", "slow"],
    "qa-voip": ["test", "regression", "reproduce", "failure"],
    "security-reliability": ["security", "secret", "auth", "tenant", "production"],
    "cartography-docs": ["document", "diagram", "architecture", "map", "cartography", "use case"],
}

def plan_investigation(request: InvestigationRequest) -> dict[str, Any]:
    text = f"{request.title} {request.description}".lower()
    selected = [role for role, tokens in ROLE_MAP.items() if any(token in text for token in tokens)]
    if not selected:
        selected = ["saylo-architect", "qa-voip", "cartography-docs"]
    tasks = [
        {"step": 1, "name": "Understand and scope", "status": "pending", "owner": "orchestrator", "checks": ["Clarify success conditions from supplied context", "Identify scope boundaries and affected surfaces"]},
        {"step": 2, "name": "Gather evidence", "status": "pending", "owner": selected[0], "checks": ["Inspect source files and logs", "Record paths/line numbers or packet numbers", "Separate evidence from hypotheses"]},
        {"step": 3, "name": "Propose minimal change or diagnosis", "status": "pending", "owner": selected[1] if len(selected) > 1 else selected[0], "checks": ["Preserve existing behavior unless defect/requirement proves otherwise", "Describe risks and rollback"]},
        {"step": 4, "name": "Verify", "status": "pending", "owner": "qa-voip", "checks": ["Run relevant tests or validators if an execution environment is available", "Record exact commands and actual outcomes"]},
        {"step": 5, "name": "Review and document", "status": "pending", "owner": "cartography-docs", "checks": ["Review security and regression impact", "Update relevant diagrams/runbooks", "Report incomplete work and unknowns"]},
    ]
    return {"id": str(uuid4()), "created_at": datetime.now(timezone.utc).isoformat(), "title": request.title, "description": request.description, "kind": request.kind, "source_paths": request.source_paths, "status": "planned", "execution_mode": "deterministic-planner", "selected_agents": selected, "tasks": tasks, "safety_gates": ["No production deploy or live phone reconfiguration", "No destructive database changes without explicit approval and recovery plan", "Do not upload source, secrets, call data, or PCAPs to an external model without approval"], "limitations": ["This endpoint creates a plan; it does not execute AI agents or modify source files.", "Model runtime and coordinated multi-agent execution are not configured in this initial scaffold."]}
