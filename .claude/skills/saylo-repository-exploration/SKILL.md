---
name: saylo-repository-exploration
description: Build an evidence-backed map of the actual Saylo source before making changes.
---
# Saylo repository exploration

1. Record repository path, branch and commit; note if the checkout is missing or empty.
2. Inventory solution/project manifests, Angular workspace, configuration files, migrations, tests, deployment and infrastructure assets while excluding generated folders and secrets.
3. Map API endpoints, DI registrations, domain services, repository/data access, database entities, background jobs, queues, Redis, and provisioning interfaces from actual references.
4. For a feature request, trace the path in both directions: frontend request/event to backend and backend state/event/config back to clients/phones.
5. Build Mermaid architecture/use-case/sequence/ER diagrams with evidence pointers. Do not infer runtime edges from file co-occurrence.
6. Report confirmed facts, assumptions, missing inputs, tests and likely risks before coding.
