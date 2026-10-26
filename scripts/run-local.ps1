$ErrorActionPreference = "Stop"
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env" }
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m app.run
