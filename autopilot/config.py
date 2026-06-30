"""
Configuration loader for AUTOPILOT.

Loads environment variables using python-dotenv when present and validates them.
"""

from dataclasses import dataclass
import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Load .env automatically if present (local development)
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Config:
    TOKEN: str
    OWNER_ID: int
    RAILWAY_TOKEN: Optional[str]
    GITHUB_TOKEN: Optional[str]

def load_config() -> Config:
    """
    Load and validate required environment variables.
    Raises RuntimeError with a clear message if required values are missing.
    """
    token = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
    owner = os.getenv("OWNER_ID")
    railway_token = os.getenv("RAILWAY_TOKEN")
    github_token = os.getenv("GITHUB_TOKEN")

    missing = []
    if not token:
        missing.append("TOKEN")
    if not owner:
        missing.append("OWNER_ID")

    if missing:
        msg = f"Missing required environment variables: {', '.join(missing)}. See .env.example"
        logger.error(msg)
        raise RuntimeError(msg)

    try:
        owner_id = int(owner)
    except Exception:
        msg = f"OWNER_ID must be an integer, got: {owner!r}"
        logger.error(msg)
        raise RuntimeError(msg)

    return Config(
        TOKEN=token,
        OWNER_ID=owner_id,
        RAILWAY_TOKEN=railway_token,
        GITHUB_TOKEN=github_token,
    )
