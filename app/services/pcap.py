"""Optional TShark-backed offline PCAP analysis. No live capture is started."""
from __future__ import annotations
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

FIELDS = ["frame.number", "frame.time_relative", "ip.src", "ip.dst", "sip.Method", "sip.Status-Code", "sip.Call-ID", "sip.CSeq.method"]

def analyze_pcap(data: bytes, max_bytes: int = 20 * 1024 * 1024) -> dict[str, Any]:
    if not data:
        return {"available": False, "error": "Uploaded capture is empty.", "frames": []}
    if len(data) > max_bytes:
        return {"available": False, "error": f"Capture is larger than the configured limit ({max_bytes} bytes).", "frames": []}
    tshark = shutil.which("tshark")
    if not tshark:
        return {"available": False, "error": "TShark was not found in PATH. Install Wireshark/TShark to decode PCAP files.", "frames": [], "bytes_received": len(data)}
    with tempfile.TemporaryDirectory(prefix="voip-ai-pcap-") as tmp:
        path = Path(tmp) / "capture.pcap"
        path.write_bytes(data)
        command = [tshark, "-n", "-r", str(path), "-Y", "sip", "-T", "fields"]
        for field in FIELDS:
            command.extend(["-e", field])
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False, shell=False)
        except subprocess.TimeoutExpired:
            return {"available": False, "error": "TShark analysis exceeded the 60-second limit.", "frames": []}
        if completed.returncode != 0:
            return {"available": False, "error": "TShark could not decode the capture.", "diagnostic": completed.stderr[-2000:], "frames": []}
        frames = []
        for line in completed.stdout.splitlines()[:5000]:
            bits = line.split("\t")
            bits += [""] * (len(FIELDS) - len(bits))
            frames.append(dict(zip(FIELDS, bits)))
        return {"available": True, "frame_count_returned": len(frames), "truncated": len(completed.stdout.splitlines()) > 5000, "frames": frames, "note": "Only SIP-filtered summary fields are returned. Verify frame numbers in Wireshark for conclusions."}
