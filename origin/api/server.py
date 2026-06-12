"""FastAPI application factory for the ORIGIN Core API layer."""

from __future__ import annotations

from fastapi import FastAPI

from origin.api.rest import router


def create_app() -> FastAPI:
    """Create and configure the ORIGIN API application."""
    app = FastAPI(title="ORIGIN", version="1.0.0")
    app.include_router(router)
    return app


app = create_app()
