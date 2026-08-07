"""Minimal .env support.

Upstream uses python-dotenv. This covers the one case that matters — a
`KEY=value` file at the repo root — without adding a dependency.
"""
from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: str | Path = ".env") -> None:
    """Load KEY=value pairs from `path`. Existing env vars always win."""
    dotenv = Path(path)
    if not dotenv.exists():
        return

    for line in dotenv.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def require_api_key(var_name: str, service_name: str) -> str:
    """Fetch an API key from the environment or .env, or explain how to set it."""
    load_dotenv()
    api_key = os.getenv(var_name)
    if not api_key:
        raise ValueError(
            f"{service_name} needs {var_name}. Either export it:\n"
            f"    export {var_name}=...\n"
            f"or add this line to a .env file at the repo root:\n"
            f"    {var_name}=..."
        )
    return api_key
