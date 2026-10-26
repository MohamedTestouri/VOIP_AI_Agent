from pathlib import Path
from app.services.project_scanner import scan_repository, build_cartography


def test_scanner_reports_indicators_without_source_snippets(tmp_path: Path):
    (tmp_path / "Program.cs").write_text("using Microsoft.EntityFrameworkCore;\n// RabbitMQ connection setup\n", encoding="utf-8")
    (tmp_path / "appsettings.json").write_text('{"Password":"do-not-return"}', encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=value", encoding="utf-8")
    inventory = scan_repository(tmp_path)
    assert inventory["exists"] is True
    assert any(item["path"] == "Program.cs" for item in inventory["files"])
    assert not any(".env" in item["path"] for item in inventory["files"])
    assert "do-not-return" not in str(inventory)
    assert any(item["category"] == "messaging" for item in inventory["indicators"])


def test_empty_source_is_explicit():
    cartography = build_cartography({"exists": False, "indicators": []})
    assert cartography["available"] is False
    assert "Configure" in cartography["mermaid"]
