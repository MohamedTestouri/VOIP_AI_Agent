# Implementation roadmap and acceptance criteria

## Phase A — Foundation (this commit)
- [x] Local API and dashboard with health status.
- [x] Specialist roles represented as explicit catalog entries.
- [x] Bounded repository inventory and conservative path/keyword indicators.
- [x] Mermaid cartography that avoids inventing runtime dependency edges.
- [x] SIP start-line/header/CSeq/Call-ID/SDP parser with basic warnings.
- [x] Optional offline TShark adapter, without live capture.
- [x] Transparent investigation planner and local JSON persistence.
- [x] Starter agent prompts/skills, docs, and unit tests.

## Phase B — Real source-code understanding
- [ ] Point `SAYLO_REPO_PATH` at a populated checkout; record branch/commit metadata.
- [ ] Parse `.sln`/`.csproj`, Angular workspace files, EF Core DbContext/migrations, controllers/endpoints, DI registrations, Hangfire jobs, RabbitMQ publishers/consumers, Redis usage, and provisioning templates.
- [ ] Build a symbol index with line-numbered evidence and tested exclusion rules.
- [ ] Add SQL schema extraction and migration summaries without connecting to production by default.
- [ ] Build a safe PCAP fixture corpus with expected frames, Call-IDs, CSeqs, and outcomes.

## Phase C — Coordinated agent execution
- [ ] Integrate a supported Claude Code/MCP runtime, with explicit user-visible tool calls and execution records.
- [ ] Add one-writer-per-worktree orchestration, patch review, test execution, and cancellation.
- [ ] Introduce model evaluations for evidence accuracy, supported conclusions, patch quality, and regression avoidance.
- [ ] Add review gates before source writes or risky commands.

## Phase D — Production readiness
- [ ] Authentication/RBAC, audit trail, persistent store, job queue, telemetry, request quotas, backup/restore, CI/CD, secret scanning, and dependency updates.
- [ ] Vendor/model/firmware compatibility matrix backed by official docs and validated devices.
- [ ] Add approval/recovery workflows for infrastructure actions; initially keep live actions disabled.

## Exit criteria for an investigation

An investigation is complete only when the report identifies scope, actual evidence, exact commands and outputs, patch/diff where applicable, tests run (or explicit reasons not run), security/backward-compatibility considerations, documentation updates, unresolved hypotheses, and rollback considerations.
