# Specialist agent roles

Specialist descriptions live in `.claude/agents/`. The role list mirrors the initial engineering plan, with boundaries that require evidence, test results, and explicit uncertainty. Agents must not share mutable worktrees or concurrently edit the same files without an orchestrator assigning ownership.
