"""Configuration loading — configs/config.yaml (tunables) + .env (secrets).

Keeps configuration and secrets out of code. Import `config()` for settings and
`secret()` for API keys.
"""


import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent  # the AgenticAI/ directory
load_dotenv(ROOT / ".env")


@lru_cache
def config() -> dict[str, Any]:
    with open(Path(__file__).resolve().parent / "config.yaml") as f:
        return yaml.safe_load(f)


def secret(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required secret {name!r} — set it in AgenticAI/.env")
    return value
