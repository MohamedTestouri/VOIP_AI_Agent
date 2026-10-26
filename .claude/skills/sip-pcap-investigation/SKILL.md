---
name: sip-pcap-investigation
description: A repeatable, evidence-first workflow for investigating SIP or supplementary-service incidents from PCAPs and logs.
---
# SIP/PCAP investigation

1. Establish the exact symptom, expected/actual behavior, time window/timezone, endpoints, device/firmware, transport, and reproduction steps.
2. Confirm the capture direction and completeness. Do not treat absent traffic as proof unless capture point, filters, and loss are known.
3. Build a timeline with frame number/time, source/destination, method/status, Call-ID, CSeq, Via branch, tags, and relevant routing headers. Redact auth headers and identities.
4. Separate transactions from dialogs. Correlate retransmissions, provisional/final responses, ACK, CANCEL, BYE, and forks correctly.
5. For SDP, compare offers/answers, connection addresses, media ports, payload types, codecs, direction attributes, and RTP observations.
6. For DND/forwarding/BLF, compare both phone-originated signaling and server-originated state/provisioning updates; note vendor/model/firmware.
7. Record an evidence table: observation, frame/path reference, interpretation, confidence, alternatives, next experiment.
8. Build a sanitized regression fixture and expected parser/behavior test.
9. Report unresolved questions and what evidence would resolve them. Never assert a root cause from one ambiguous packet.
