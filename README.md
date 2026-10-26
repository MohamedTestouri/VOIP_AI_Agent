# VoIP AI Engineering Team

An evidence-driven local workspace for VoIP investigations and the Saylo platform. This foundation combines a FastAPI service, lightweight dashboard, deterministic repository inventory, SIP/SDP parser, optional offline TShark adapter, transparent investigation planner, Claude Code specialist agents/skills, tests, and operational documentation.

> **Important:** The GitHub reference repository `MohamedTestouri/Saylo_Platform` was empty at discovery time. This project therefore does not claim to know Saylo's actual source architecture. Configure `SAYLO_REPO_PATH` to a populated local checkout to generate repository-specific evidence and maps.

## Features

- **Local dashboard** for project status, source inventory, agent roles, cartography, investigation planning, SIP parsing, and optional PCAP analysis.
- **SIP/SDP parser** for request/response start lines, Call-ID, CSeq, Via branch, From/To tags, Contact, content type, SDP connection/media/codec attributes, and basic warnings. Authentication/challenge headers are omitted.
- **Repository scanner** with bounded traversal, exclusions for generated directories and sensitive files, and conservative path/keyword indicators. It returns evidence paths, not source snippets.
- **Offline PCAP analysis** through TShark when installed. No live capture is initiated. PCAP data is size-limited, processed in a temporary directory and not saved by the API.
- **Transparent deterministic planner** to record task plans in local JSON. It explicitly does not pretend model agents executed or changed code.
- **Nine specialist roles** and six initial skills covering VoIP protocol investigation, Kamailio, Saylo exploration, provisioning, feature engineering, QA, security, and documentation cartography.
- **Safety guidance, Mermaid architecture, roadmap, tests, and GitHub Actions CI.**

## Quick start

Requirements: Python 3.11+ (3.12 recommended). TShark is optional.

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Copy `.env.example` to `.env`, then set `SAYLO_REPO_PATH` to the local path of your Saylo source checkout. Start the service:

```bash
python -m app.run
```

Open <http://127.0.0.1:8000>. API documentation is at <http://127.0.0.1:8000/docs>.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m python -m app.run
```

Or use `scripts/run-local.ps1` / `scripts/run-local.sh` from the project root.

## Push to the destination repository

The current ChatGPT GitHub connection rejected repository writes with HTTP 403, so this session could not push the files directly. Once you have extracted this ZIP and configured local GitHub authentication (`gh auth login` or Git credential manager), run `scripts/push-to-github.ps1` on Windows or `./scripts/push-to-github.sh` on macOS/Linux from the project root. The scripts initialize `main` if needed, verify the configured `origin`, create a commit, and push without force-pushing. If the remote is not empty or has diverged, stop and reconcile the history rather than overwriting it.

## Configuration

| Variable | Purpose |
|---|---|
| `APP_HOST` | Recommended `127.0.0.1`; exposing the dashboard requires authentication and TLS |
| `APP_PORT` | Local service port; default `8000` |
| `SAYLO_REPO_PATH` | Local path to a populated Saylo checkout |
| `DATA_DIR` | Local persisted investigation records; default `./data` |
| `MAX_SCAN_FILES` | Maximum files inventoried in a scan |
| `MAX_PCAP_BYTES` | Maximum PCAP body size; default 20 MiB |

The current version does not call an external model provider. Agent role definitions are ready for a future Claude Code or other controlled runtime, but the current API only plans investigations and runs deterministic tools.

## Project layout

```text
app/                     FastAPI routes, configuration, agent catalog, analysis services
dashboard/               Static engineering dashboard
.claude/agents/           Specialist agent definitions
.claude/skills/           Repeatable VoIP/Saylo engineering procedures
CLAUDE.md                 Persistent project instructions for Claude Code
docs/                     Architecture, Claude Code setup, evidence, safety, status, roadmap
tests/                    Unit tests for deterministic logic
scripts/                  Local launch helpers
data/                     Local artifacts; generated content is ignored by Git
```

## Evidence rules

Mark each claim as observed evidence, inference, hypothesis, or unknown. Link findings to source paths/line numbers, configuration keys, packet frame/time, requests/responses, schema objects, and test results. Co-occurring words or files are leads, not proof of runtime dependencies. A task is not complete only because code was generated; relevant validation and actual test outcomes must be recorded.

## Safety and limitations

- Local development only; no authentication or production hardening is included.
- No production deployments, live Kamailio reloads, destructive DB actions, or phone provisioning/resync are implemented.
- PCAP summaries may still contain sensitive IPs, Call-IDs, or addressing; review/redact before sharing.
- Inventory is heuristic and bounded, not a full static analyzer. Generated diagrams must be reviewed.
- Do not commit `.env`, customer data, credentials, real SIP authentication material, DB backups, PCAPs, or production configuration.
- Review external skills/tools before installation and execution. Do not expose private project material to external providers without approval.

## Tests

```bash
pytest -q
```

## Next milestones

1. Populate the Saylo source checkout and capture its commit/branch metadata.
2. Replace keyword heuristics with parsers for the actual .NET/Angular, schema/migrations, jobs, broker events, Kamailio configs, and provisioning templates present.
3. Build a sanitized known-incident/PCAP regression corpus.
4. Add a controlled agent runtime and per-task worktree isolation, with approval gates before writes.
5. Add authentication, audit history, queueing, model evaluation, dependency/security scanning, backups, and deployment controls before shared hosting.
