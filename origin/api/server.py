"""FastAPI application factory for the ORIGIN Core API layer with causal decision endpoint."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel
import logging
from typing import Any, Dict

from origin.api.rest import router

# Import causal engine (may raise ImportError if module missing)
try:
    from origin.decision_engine.causal_engine import compile_causal_engine
except Exception:  # pragma: no cover - import may fail in tests/environments
    compile_causal_engine = None

logger = logging.getLogger(__name__)


class DecisionRequest(BaseModel):
    payload: Dict[str, Any]


def create_app() -> FastAPI:
    """Create and configure the ORIGIN API application."""
    app = FastAPI(title="ORIGIN", version="1.0.0")
    app.include_router(router)

    # Mount causal decision endpoint directly on the app so it appears in OpenAPI

    @app.post(
        "/v1/decision/causal",
        summary="Run causal decision engine",
        description=(
            "Execute the compiled ORIGIN causal decision graph on the provided payload. "
            "Returns JSON with status=success and the engine output on success, or status=fallback if an internal failure occurred."
        ),
        response_description="Causal decision execution result",
        responses={
            200: {"description": "Execution result"},
            500: {"description": "Engine error"},
        },
    )
    async def causal_decision_endpoint(req: DecisionRequest):
        """Endpoint wrapper that delegates to run_causal_decision.

        Request body example:
        {
            "payload": {
                "incident_description": "..."
            }
        }
        """
        try:
            result = await run_causal_decision(req.payload)
            if result is None:
                # Unexpected failure
                return JSONResponse(status_code=200, content={"status": "fallback", "result": None})

            status = "success" if result.get("final_decision") else "fallback"
            return {"status": status, "result": _serialize_result(result)}

        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Causal decision endpoint failed: %s", exc)
            # On any exception return fallback status and the error message
            return JSONResponse(status_code=200, content={"status": "fallback", "error": str(exc)})

    return app


app = create_app()


async def run_causal_decision(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    """Run the causal engine with the provided payload and return the raw engine output.

    Returns None if the compile step or invocation is not available.
    """
    if compile_causal_engine is None:
        logger.error("Causal engine is not available (compile_causal_engine import failed)")
        return None

    try:
        graph = compile_causal_engine()
        # graph.ainvoke is expected to be an async method that takes the payload/state
        result = await graph.ainvoke(payload)
        return result
    except Exception as exc:  # pragma: no cover - bubble up handled by caller
        logger.exception("Error running causal engine: %s", exc)
        # Return a structured fallback response
        return {"final_decision": None, "errors": [str(exc)]}


def _serialize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize engine objects (like Pydantic models) to plain JSON-serializable dicts."""
    serialized: Dict[str, Any] = {}
    for k, v in result.items():
        try:
            # Pydantic BaseModel support
            if hasattr(v, "dict") and callable(getattr(v, "dict")):
                serialized[k] = v.dict()
            else:
                serialized[k] = v
        except Exception:
            # Fall back to string repr
            serialized[k] = str(v)
    return serialized
