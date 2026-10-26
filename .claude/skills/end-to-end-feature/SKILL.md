---
name: end-to-end-feature
description: Safely implement and verify a bounded feature across application layers.
---
# End-to-end feature implementation

1. Write acceptance criteria and reproduce current behavior.
2. Map the existing flow and identify the smallest cross-layer change set.
3. Identify authorization, validation, tenant boundaries, idempotency, failure, timeout, retry and concurrency semantics.
4. Implement in repository conventions. Do not introduce architecture or packages without a concrete need.
5. Add targeted unit/integration/regression tests, including negative cases.
6. Run the appropriate build, lint, test and config validation commands; capture real exit status.
7. Review diff for unrelated changes, secrets, migrations, backward compatibility and observability.
8. Update API docs, use case, sequence/data-flow diagrams and runbook if behavior changed.
9. Deliver files changed, evidence, commands/results, limitations and rollback.
