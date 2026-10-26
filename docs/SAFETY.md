# Safety and data-handling rules

1. **Local by default.** Keep `APP_HOST=127.0.0.1`. Do not expose the UI on a network without authentication, TLS, authorization, request limits, and a threat model.
2. **No production mutation.** Agents may propose diffs and instructions, but production DB changes, Kamailio reloads, firmware pushes, phone resyncs, and deployments require explicit operator authorization and a tested rollback plan.
3. **Handle secrets deliberately.** Never commit `.env`, credentials, SIP passwords, authorization headers, private keys, production config, databases, recordings, packet captures, or customer data. The inventory deliberately skips common sensitive files and returns file paths only, not text snippets.
4. **PCAP minimization.** PCAP uploads are limited by `MAX_PCAP_BYTES`, written into a temporary directory, and deleted on request completion. The output includes only selected SIP fields and may still contain sensitive IPs, Call-IDs, or addressing; do not publish it without review.
5. **Evidence over confidence.** Label observations, inferences, and hypotheses separately. Provide file path/line references or packet frame/time whenever possible. Unknown is an acceptable result.
6. **External AI is opt-in.** The initial project does not transmit data to a model. Any future model integration must define approved data classes, redaction, retention, provider, budget, and opt-out controls first.
7. **Least privilege.** Use read-only DB credentials for diagnostics. Add parameterization, allowlists, timeouts, request bounds, and audit logs to any future tools that touch infrastructure.
8. **Reversible changes.** Prefer small diffs, tests, snapshots, backups, and isolated environments. Do not install unreviewed skills or run downloaded scripts without inspecting their source.

## Before any shared deployment

- Add authentication and role-based authorization.
- Review all endpoints and file-upload paths.
- Add audit events and retention policy.
- Threat-model SSRF, path traversal, prompt injection, secret exposure, and malicious repository content.
- Add CI, dependency scanning, rate limits, and deployment rollback.
