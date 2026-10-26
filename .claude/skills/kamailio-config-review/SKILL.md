---
name: kamailio-config-review
description: Trace and safely review Kamailio configuration changes.
---
# Kamailio configuration review

1. Record Kamailio version and loaded modules; use version-matched documentation.
2. Trace SIP request path from entry routing block through route calls, transaction creation, authentication, NAT, dispatcher and failure handling.
3. Search for variable/flag reads and writes before changing semantics.
4. Explain condition ordering and how each message method/status is handled. Cite file and line.
5. Validate syntax/config with the matching `kamailio -c` invocation in a non-production environment if available.
6. Review security, loops, retransmissions, dialog state, routing headers, transport constraints and rollback.
7. Do not reload/restart a live proxy or deploy without operator authorization.
