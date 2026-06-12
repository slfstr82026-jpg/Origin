"""Command-line entry point for ORIGIN."""

from __future__ import annotations

from origin.api.server import create_app


def main() -> None:
    """Print startup guidance for the ORIGIN service."""
    create_app()
    print("ORIGIN app created. Run with: uvicorn origin.api.server:app")


if __name__ == "__main__":
    main()
