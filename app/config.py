"""Environment configuration with safe local defaults."""
from __future__ import annotations
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load local configuration without overriding explicitly exported environment variables.
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env", override=False)
except ImportError:
    pass

def repo_path() -> Path | None:
    raw = os.getenv("SAYLO_REPO_PATH", "").strip()
    if not raw:
        return None
    candidate = Path(raw).expanduser().resolve()
    return candidate if candidate.exists() and candidate.is_dir() else candidate

def data_path() -> Path:
    raw = os.getenv("DATA_DIR", "./data").strip() or "./data"
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()

def integer_setting(name: str, default: int, minimum: int = 1) -> int:
    try:
        return max(minimum, int(os.getenv(name, str(default))))
    except (TypeError, ValueError):
        return default
