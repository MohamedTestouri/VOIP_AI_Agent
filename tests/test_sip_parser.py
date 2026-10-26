from app.services.sip_parser import parse_sip_message


def test_parses_sip_invite_and_sdp():
    message = "\r\n".join([
        "INVITE sip:1008@example.test SIP/2.0",
        "Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bKabc",
        "From: <sip:1005@example.test>;tag=from1",
        "To: <sip:1008@example.test>",
        "Call-ID: call-1@example.test",
        "CSeq: 3 INVITE",
        "Content-Type: application/sdp",
        "",
        "v=0",
        "c=IN IP4 192.0.2.10",
        "m=audio 20000 RTP/AVP 0 8 101",
        "a=rtpmap:0 PCMU/8000",
        "",
    ])
    parsed = parse_sip_message(message)
    assert parsed["valid_start_line"] is True
    assert parsed["method"] == "INVITE"
    assert parsed["call_id"] == "call-1@example.test"
    assert parsed["cseq"] == {"number": 3, "method": "INVITE"}
    assert parsed["from_tag"] == "from1"
    assert parsed["via_branch"] == "z9hG4bKabc"
    assert parsed["sdp"]["media"][0]["port"] == "20000"
    assert parsed["sdp"]["connection_addresses"] == ["192.0.2.10"]


def test_parses_response_and_omits_auth_headers():
    message = "\r\n".join([
        "SIP/2.0 401 Unauthorized",
        "Call-ID: c1",
        "CSeq: 7 REGISTER",
        "WWW-Authenticate: Digest realm=secret",
        "",
        "",
    ])
    parsed = parse_sip_message(message)
    assert parsed["status_code"] == 401
    assert parsed["cseq"]["method"] == "REGISTER"
    assert parsed["security_note"]
    assert parsed["warnings"]
    assert "secret" not in str(parsed)


def test_unknown_start_line_is_reported():
    message = "\r\n".join(["not SIP", "X-Header: v", "", ""])
    parsed = parse_sip_message(message)
    assert parsed["message_type"] == "unknown"
    assert parsed["valid_start_line"] is False
    assert parsed["warnings"]
