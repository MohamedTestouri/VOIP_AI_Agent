"""Local launcher that reads APP_HOST and APP_PORT from .env/environment."""
from __future__ import annotations
import os
import uvicorn
from app.config import PROJECT_ROOT  # Importing config loads the local .env file.

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("APP_PORT", "8000"))
    except ValueError:
        port = 8000
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
