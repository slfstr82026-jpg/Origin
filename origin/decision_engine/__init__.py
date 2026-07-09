"""Decision engine package exports."""

from .workflow_engine import WorkflowEngine, Workflow, Step, make_step, noop_action

# Re-export causal engine compile function if present
try:
    from .causal_engine import compile_causal_engine, CausalDecisionSchema, EngineState  # type: ignore
except Exception:  # pragma: no cover - optional import
    # If causal_engine is not yet created, ignore import error during packaging
    compile_causal_engine = None

__all__ = [
    "WorkflowEngine",
    "Workflow",
    "Step",
    "make_step",
    "noop_action",
    "compile_causal_engine",
    "CausalDecisionSchema",
    "EngineState",
]
