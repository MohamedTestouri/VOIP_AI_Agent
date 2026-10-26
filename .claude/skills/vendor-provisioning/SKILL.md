---
name: vendor-provisioning
description: Investigate phone provisioning and vendor/model/firmware compatibility.
---
# Phone provisioning investigation

1. Identify manufacturer, exact model, firmware, account/line, transport and provisioning protocol.
2. Trace the actual template selection, model data, generated config URL, request/response, content type, cache behavior and device resync trigger.
3. Compare before/after generated config while redacting credentials, auth tokens, MACs and user data.
4. Use packet capture/request logs to distinguish delivery success from device application success; HTTP 200 alone does not prove config was accepted.
5. Consult official vendor docs for the exact firmware family and test on a lab device.
6. Add a fixture/assertion for the intended setting and a matrix row for model/firmware.
7. Do not trigger resync/reboot or firmware updates on live phones without explicit approval and recovery plan.
