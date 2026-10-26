# Claude Code integration setup

This repository includes project-scoped custom subagents and skills in the documented Claude Code layout:

- `.claude/agents/*.md` — specialist subagents with YAML frontmatter and focused instructions.
- `.claude/skills/<name>/SKILL.md` — reusable procedures Claude can load when relevant or invoke as `/skill-name`.
- `CLAUDE.md` — persistent project instructions loaded into Claude Code sessions.

Official references (check these for the current supported fields and runtime behavior):

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

## Start a session

1. Install/update Claude Code according to Anthropic's official installation documentation.
2. Open a terminal at this repository root and run `claude`.
3. Review the project permissions presented by Claude Code. Do not broadly approve production-impacting shell, database, or network commands.
4. Confirm `/agents` lists the specialist definitions and that the skills are discoverable via `/` (exact UX may vary by Claude Code version).
5. Ask the principal orchestrator to inspect the checkout, build an evidence-based architecture map, and run existing tests before attempting a feature.
6. Use a clean Git worktree or branch for implementation tasks and one writer per file set. Have independent agents perform read-only investigation in parallel when useful.

## Limits of this repository scaffold

The dashboard's API does not invoke Claude Code or these subagents. The project-scoped agent/skill files are consumed by the Claude Code runtime in a session started from this repository. The current API remains a deterministic planner and analysis toolkit, and does not impersonate an executed LLM. A future programmatic orchestration service should use a supported Claude Agent SDK/MCP runtime, explicit permissions, audit records, cancellation, per-task worktrees, evaluation fixtures, and approval gates.
