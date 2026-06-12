"""Runtime configuration for ORIGIN."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Filesystem settings used by the runtime."""

    data_dir: Path = Path("data")
    graph_store: Path = Path("data/graph_store.json")


def load_settings() -> Settings:
    """Load default settings."""
    return Settings()
