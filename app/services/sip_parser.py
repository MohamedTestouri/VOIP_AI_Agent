"""Conservative SIP/SDP parser for sanitized text and packet-derived payloads."""
from __future__ import annotations
import re
from typing import Any

_SENSITIVE_HEADERS = {"authorization", "proxy-authorization", "www-authenticate", "proxy-authenticate"}

def _unfold_headers(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in lines:
        if line[:1] in (" ", "\t") and result:
            result[-1] += " " + line.strip()
        else:
            result.append(line)
    return result

def _header_map(lines: list[str]) -> dict[str, list[str]]:
    headers: dict[str, list[str]] = {}
    for line in _unfold_headers(lines):
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        key = name.strip().lower()
        if key and key not in _SENSITIVE_HEADERS:
            headers.setdefault(key, []).append(value.strip())
    return headers

def _first(headers: dict[str, list[str]], *names: str) -> str | None:
    for name in names:
        values = headers.get(name.lower())
        if values:
            return values[0]
    return None

def _tag(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"(?:^|;)\s*tag=([^;>\s]+)", value, re.IGNORECASE)
    return match.group(1) if match else None

def parse_sip_message(message: str) -> dict[str, Any]:
    text = message.replace("\r\n", "\n").replace("\r", "\n")
    header_part, separator, body = text.partition("\n\n")
    lines = header_part.split("\n")
    start_line = lines[0].strip() if lines else ""
    headers = _header_map(lines[1:])
    request_match = re.match(r"^([A-Z]+)\s+(\S+)\s+SIP/2\.0$", start_line, re.IGNORECASE)
    response_match = re.match(r"^SIP/2\.0\s+(\d{3})(?:\s+(.*))?$", start_line, re.IGNORECASE)
    method = request_match.group(1).upper() if request_match else None
    request_uri = request_match.group(2) if request_match else None
    status_code = int(response_match.group(1)) if response_match else None
    reason = (response_match.group(2) or "").strip() if response_match else None

    cseq = _first(headers, "cseq")
    cseq_match = re.match(r"^(\d+)\s+([A-Za-z]+)", cseq or "")
    via = _first(headers, "via", "v")
    via_branch = re.search(r"(?:^|;)\s*branch=([^;\s]+)", via or "", re.IGNORECASE)
    from_value = _first(headers, "from", "f")
    to_value = _first(headers, "to", "t")
    content_type = _first(headers, "content-type", "c")
    media: list[dict[str, Any]] = []
    connection_addresses: list[str] = []
    rtp_maps: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("c="):
            match = re.match(r"c=IN\s+(IP4|IP6)\s+(\S+)", line, re.IGNORECASE)
            if match:
                connection_addresses.append(match.group(2))
        elif line.startswith("m="):
            bits = line[2:].split()
            if len(bits) >= 3:
                media.append({"type": bits[0], "port": bits[1], "transport": bits[2], "formats": bits[3:]})
        elif line.startswith("a=rtpmap:"):
            rtp_maps.append(line[9:])

    warnings: list[str] = []
    if not request_match and not response_match:
        warnings.append("The first line is not a recognized SIP request or response line.")
    if not _first(headers, "call-id", "i"):
        warnings.append("Call-ID is absent; correlate this message using other packet evidence.")
    if not cseq_match:
        warnings.append("CSeq is absent or malformed.")
    if media and not content_type:
        warnings.append("SDP-like media lines exist but Content-Type is missing.")
    if status_code is not None and status_code >= 400:
        warnings.append("SIP response is an error response; inspect reason, transaction, and neighboring messages.")

    return {
        "valid_start_line": bool(request_match or response_match),
        "start_line": start_line,
        "message_type": "request" if request_match else "response" if response_match else "unknown",
        "method": method,
        "request_uri": request_uri,
        "status_code": status_code,
        "reason_phrase": reason,
        "call_id": _first(headers, "call-id", "i"),
        "cseq": {"number": int(cseq_match.group(1)), "method": cseq_match.group(2).upper()} if cseq_match else None,
        "via": via,
        "via_branch": via_branch.group(1) if via_branch else None,
        "from": from_value,
        "from_tag": _tag(from_value),
        "to": to_value,
        "to_tag": _tag(to_value),
        "contact": _first(headers, "contact", "m"),
        "content_type": content_type,
        "content_length": _first(headers, "content-length", "l"),
        "sdp": {"connection_addresses": connection_addresses, "media": media, "rtp_map_attributes": rtp_maps},
        "warnings": warnings,
        "security_note": "Authorization and challenge headers are intentionally omitted from parsed output.",
        "body_present": bool(separator and body.strip()),
    }
