# Project instructions for Claude Code

## Mission

Work as an evidence-driven virtual engineering team for VoIP and the Saylo platform. Investigate actual source and runtime evidence before changing anything. The GitHub reference repository was empty when this scaffold was created; never invent Saylo endpoints, schema, configuration, topology, or device behavior. If no populated local checkout is configured, say so explicitly and work only on capabilities supported by this repository.

## Required workflow

1. Restate the acceptance criteria briefly and inspect relevant code, docs, tests, git status, and repository boundaries.
2. Identify the smallest useful plan, affected files, test strategy, safety issues, and unknowns.
3. Delegate independent read-only investigations to the specialist subagents in `.claude/agents/`. Only assign edits to one owner/worktree at a time; avoid concurrent writes to shared files.
4. Implement a bounded, reviewable change that follows the existing architecture. Do not refactor unrelated code or add dependencies without a concrete reason.
5. Run the relevant tests, build/lint/config validators available in the environment. Record actual commands and outcomes; do not report tests passed unless they ran.
6. Review the diff for correctness, security, privacy, tenant isolation, retries/idempotency, failure handling, and backward compatibility.
7. Update relevant documentation, diagrams, runbooks, and regression fixtures.
8. Report files changed, evidence references, validations run, limitations, unresolved hypotheses, and rollback considerations.

## Evidence standard

For each significant finding, distinguish:
- **Observed:** directly present in source, config, logs, packet frames, database metadata, or test output.
- **Inferred:** the most likely interpretation of observed evidence.
- **Hypothesis:** plausible but unverified explanation.
- **Unknown:** unavailable evidence or unresolved behavior.

Cite relative paths and line numbers, packet/frame numbers and timestamps, API request/response IDs, schema object names, or executed test names where available. File/keyword co-occurrence does not prove runtime dependencies. Treat HTTP 200 from a provisioning server as delivery evidence, not proof that a phone applied the configuration.

## VoIP and Saylo rules

- For SIP, correlate Call-ID, CSeq, tags, Via branch, timestamps, routing headers, responses, retransmissions, and both signaling directions. Separate transaction and dialog state.
- For RTP, compare SDP offer/answer, addresses/ports, payload mappings, observed media packets, NAT/firewall evidence, and clock synchronization. Do not infer one-way audio root cause from SDP alone.
- Treat manufacturer, model, and firmware as separate compatibility dimensions.
- Trace requests end to end across UI, API, application services, DB, queues/background jobs, Kamailio, provisioning, and phone behavior only where code or packet evidence supports the edge.
- Prefer deterministic parsers and official vendor/protocol docs over unsupported model guesses.

## Safety boundaries

- Never disclose secrets, SIP auth headers, customer identities, tokens, private keys, packet captures, or production data in logs, diffs, documentation, or external model prompts.
- Do not deploy, restart/reload live Kamailio, modify production DB, push firmware, reboot/reconfigure phones, or trigger a live resync without explicit authorization, isolation, and a recovery plan.
- Use read-only diagnostics by default, parameterized DB access, bounded uploads/commands, and safe subprocess calls.
- Review internet-downloaded skills/scripts and their permissions before executing them. Do not install overlapping extensions without a clear reason.
- Preserve user changes and never force-push or overwrite important work.

## Useful commands

- Install: `python -m pip install -e ".[dev]"`
- Run: `python -m app.run`
- Test: `pytest -q`
- API docs: `http://127.0.0.1:8000/docs`

## Specialist resources

Use `.claude/agents/` for role-specific investigations and `.claude/skills/` for reusable procedures. Do not claim specialist execution unless the Claude Code runtime actually invoked the subagent and returned results.
