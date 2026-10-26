from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.agents import AGENTS
from app.config import PROJECT_ROOT, data_path, integer_setting, repo_path
from app.schemas import InvestigationRequest, SipParseRequest
from app.services.investigations import plan_investigation
from app.services.pcap import analyze_pcap
from app.services.project_scanner import build_cartography, scan_repository
from app.services.sip_parser import parse_sip_message

app = FastAPI(title="VoIP AI Engineering Team", version="0.1.0", description="Local, evidence-driven VoIP/Saylo engineering workspace")
DASHBOARD = PROJECT_ROOT / "dashboard"
app.mount("/static", StaticFiles(directory=str(DASHBOARD)), name="static")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(DASHBOARD / "index.html")

@app.get("/api/health")
def health() -> dict[str, Any]:
    path = repo_path()
    return {"status": "ok", "service": "voip-ai-engineering-team", "version": app.version, "saylo_repo_configured": bool(path and path.exists() and path.is_dir()), "tshark_available": __import__("shutil").which("tshark") is not None, "model_runtime": "not configured; deterministic tools only"}

@app.get("/api/agents")
def list_agents() -> dict[str, Any]:
    return {"agents": AGENTS, "count": len(AGENTS), "note": "These are role definitions, not a claim that agents have executed."}

@app.get("/api/project/inventory")
def project_inventory() -> dict[str, Any]:
    try:
        return scan_repository()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inventory failed: {type(exc).__name__}") from exc

@app.get("/api/project/cartography")
def project_cartography() -> dict[str, Any]:
    return build_cartography(scan_repository())

@app.post("/api/voip/sip/parse")
def sip_parse(payload: SipParseRequest) -> dict[str, Any]:
    return parse_sip_message(payload.message)

@app.post("/api/voip/pcap/analyze")
async def pcap_analyze(request: Request) -> dict[str, Any]:
    content_type = request.headers.get("content-type", "").lower()
    if "application/octet-stream" not in content_type and "pcap" not in content_type:
        raise HTTPException(status_code=415, detail="Send the capture as raw bytes with Content-Type: application/octet-stream.")
    max_bytes = integer_setting("MAX_PCAP_BYTES", 20 * 1024 * 1024)
    announced_length = request.headers.get("content-length")
    if announced_length:
        try:
            if int(announced_length) > max_bytes:
                raise HTTPException(status_code=413, detail=f"Capture exceeds the configured limit of {max_bytes} bytes.")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Content-Length header.")
    chunks: list[bytes] = []
    total = 0
    async for chunk in request.stream():
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(status_code=413, detail=f"Capture exceeds the configured limit of {max_bytes} bytes.")
        chunks.append(chunk)
    return analyze_pcap(b"".join(chunks), max_bytes=max_bytes)

@app.post("/api/investigations", status_code=201)
def create_investigation(payload: InvestigationRequest) -> dict[str, Any]:
    record = plan_investigation(payload)
    root = data_path() / "investigations"
    root.mkdir(parents=True, exist_ok=True)
    destination = root / f"{record['id']}.json"
    # Use exclusive create to avoid overwriting existing records.
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    return record

@app.get("/api/investigations")
def list_investigations() -> dict[str, Any]:
    root = data_path() / "investigations"
    if not root.exists():
        return {"investigations": []}
    records = []
    for path in sorted(root.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:100]:
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            continue
    return {"investigations": records}
