# VoIP evidence collection guide

## SIP message analysis

Capture for each message: packet/frame number and timestamp, transport, source/destination tuple, request method or response status, Call-ID, CSeq number/method, Via branch, From/To tags, relevant Route/Record-Route/Contact, and body content type. Redact credentials and private identities before sharing.

Use Call-ID together with CSeq, tags, timestamps, and Via branch; Call-ID alone is not always sufficient to distinguish transaction behavior. Preserve the difference between a SIP transaction and a dialog. For TCP/TLS, account for stream reassembly/decryption requirements before concluding that messages are missing.

## SDP/RTP

Record `c=` connection addresses, `m=` media/port/protocol/formats, payload type to `a=rtpmap` mappings, direction attributes, codec negotiation, and whether the negotiated media address/port matches observed RTP. Do not infer one-way audio root cause from SDP alone; validate NAT, firewall, symmetric RTP, RTP flow, codec, and timing evidence.

## Supplementary services

For DND, call forwarding, BLF, transfer, and related behavior, collect both directions where available: phone-to-platform signaling and platform-to-phone state/config updates. Include make/model, firmware, transport, registration state, relevant config version, Call-ID/dialog details, and before/after server-side state. Treat each vendor/model/firmware as a separate compatibility target until tested.

## Reproducible incident bundle

- Symptom, expected result, actual result, exact reproduction sequence.
- Device model, firmware, line/account identity redacted, transport and network topology.
- Time range and timezone; synchronized clock status.
- Sanitized PCAP, logs, relevant config before/after, and request correlation identifiers.
- Working vs failing device/control experiment.
- Hypotheses with an evidence table and a regression test plan.

## TShark availability

The application checks for `tshark` on PATH and decodes offline captures only. If absent, install Wireshark/TShark from the official distribution source and verify the binary version before use. No capture is started by the application.
