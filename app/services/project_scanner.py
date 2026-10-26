"""Safe, bounded repository inventory and conservative cartography hints."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from app.config import integer_setting, repo_path

EXCLUDED_DIRS = {".git", ".hg", ".svn", "node_modules", "vendor", "bin", "obj", ".venv", "venv", "__pycache__", ".angular", "dist", "build", "coverage", "packages"}
SENSITIVE_NAMES = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519", "credentials.json", "secrets.json", "appsettings.production.json"}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".pcap", ".pcapng", ".cap", ".dump", ".bak", ".db", ".sqlite", ".sql"}
TEXT_SUFFIXES = {".cs", ".csproj", ".sln", ".json", ".xml", ".yml", ".yaml", ".toml", ".md", ".ts", ".html", ".scss", ".js", ".cfg", ".conf", ".ini", ".sh", ".ps1", ".sql", ".dockerfile", ".py", ".txt", ".props", ".targets"}


def _is_sensitive(path: Path) -> bool:
    return path.name.lower() in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES or any(token in path.name.lower() for token in ("secret", "credential", "password", "private_key"))

def scan_repository(root: Path | None = None) -> dict[str, Any]:
    configured = root is not None or repo_path() is not None
    root = root or repo_path()
    if root is None:
        return {"configured": False, "exists": False, "root": None, "file_count": 0, "scanned_file_count": 0, "truncated": False, "files": [], "indicators": [], "notes": ["Set SAYLO_REPO_PATH to a local checkout. The configured source repository was empty at scaffold creation time; no code-specific claims are made."]}
    root = root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return {"configured": True, "exists": False, "root": str(root), "file_count": 0, "scanned_file_count": 0, "truncated": False, "files": [], "indicators": [], "notes": ["Configured repository path does not exist or is not a directory."]}

    limit = integer_setting("MAX_SCAN_FILES", 20000)
    files: list[dict[str, Any]] = []
    indicators: list[dict[str, str | int]] = []
    total = 0
    truncated = False
    interesting = {
        "kamailio": ("kamailio.cfg", "route[", "loadmodule", "modparam"),
        "sip_or_voip": ("sip", "rtp", "callforward", "call_forward", "dnd", "blf", "provision"),
        "dotnet": (".csproj", ".sln", "program.cs", "startup.cs", "entityframeworkcore"),
        "angular": ("angular.json", "app.module.ts", "provideRouter", "@angular/"),
        "messaging": ("rabbitmq", "hangfire", "redis", "rabbit", "backgroundservice"),
        "tests": ("test", "spec.ts", "xunit", "nunit", "mstest"),
        "database": ("migration", "dbcontext", "schema", "flyway", "liquibase"),
        "containers_ci": ("dockerfile", "docker-compose", ".github/workflows", "helm", "terraform"),
    }
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith("."))
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            if path.is_symlink() or _is_sensitive(path):
                continue
            total += 1
            if len(files) >= limit:
                truncated = True
                break
            relative = path.relative_to(root).as_posix()
            try:
                size = path.stat().st_size
            except OSError:
                continue
            entry: dict[str, Any] = {"path": relative, "suffix": path.suffix.lower(), "size_bytes": size}
            files.append(entry)
            path_lower = relative.lower()
            for category, tokens in interesting.items():
                hit = next((token for token in tokens if token in path_lower), None)
                if hit:
                    indicators.append({"category": category, "path": relative, "evidence": f"path matches '{hit}'"})
            if path.suffix.lower() in TEXT_SUFFIXES and size <= 1_000_000:
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                low = content.lower()
                for category, tokens in interesting.items():
                    if any(token in low for token in tokens):
                        # Do not return source snippets or secret-like values; only provide path-level signals.
                        if not any(x["category"] == category and x["path"] == relative for x in indicators):
                            indicators.append({"category": category, "path": relative, "evidence": "keyword signal in text file; review manually"})
        if truncated:
            break
    indicators.sort(key=lambda x: (str(x["category"]), str(x["path"])))
    return {"configured": configured, "exists": True, "root": str(root), "file_count": total, "scanned_file_count": len(files), "truncated": truncated, "files": files, "indicators": indicators, "notes": ["Heuristic signals are leads for review, not proof of runtime behavior.", "Secret-like files and packet captures are skipped; source text is not returned by this endpoint.", "Generated maps may be incomplete if MAX_SCAN_FILES is reached."]}


def build_cartography(inventory: dict[str, Any]) -> dict[str, Any]:
    if not inventory.get("exists"):
        return {"available": False, "summary": "Source checkout not configured or unavailable.", "components": [], "edges": [], "mermaid": "flowchart LR\n  A[Configure SAYLO_REPO_PATH] --> B[Run inventory]", "gaps": ["No repository evidence available."]}
    by_category: dict[str, set[str]] = {}
    for item in inventory.get("indicators", []):
        by_category.setdefault(str(item["category"]), set()).add(str(item["path"]))
    labels = {"dotnet": ".NET indicators", "angular": "Angular indicators", "database": "Database indicators", "messaging": "Messaging/background jobs", "kamailio": "Kamailio indicators", "sip_or_voip": "VoIP/provisioning indicators", "tests": "Test indicators", "containers_ci": "Container/CI indicators"}
    components = [{"id": key, "label": labels.get(key, key), "evidence_files": sorted(paths)[:20], "evidence_count": len(paths)} for key, paths in sorted(by_category.items())]
    # No dependency edges are inferred from co-occurrence alone.
    lines = ["flowchart TB", "  repo[Source checkout]"]
    for component in components:
        lines.append(f"  {component['id'].replace('-', '_')}[{component['label']}]:::observed")
        lines.append(f"  repo --> {component['id'].replace('-', '_')}")
    lines.append("  classDef observed fill:#eef2ff,stroke:#6366f1,color:#111827")
    return {"available": True, "summary": "Component indicators are derived from file paths and text keywords. Edges to the repository indicate discovery only, not runtime dependency.", "components": components, "edges": [], "mermaid": "\n".join(lines), "gaps": ["Runtime dependencies have not been proven by this heuristic scan.", "No source checkout-specific mapping should be treated as complete until reviewed."]}
