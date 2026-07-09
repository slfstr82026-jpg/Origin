"""Decision workflow engine placeholder for ORIGIN.

This module provides a minimal WorkflowEngine class and supporting dataclasses
as a starting point. Implement domain-specific execution, persistence, and
integration with the rest of the ORIGIN system as needed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Step:
    id: str
    action: Callable[[Dict[str, Any]], Dict[str, Any]]
    name: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Workflow:
    id: str
    steps: List[Step]
    context: Dict[str, Any] = field(default_factory=dict)


class WorkflowEngine:
    """A small, synchronous workflow executor used as a stub for decision logic.

    This engine executes steps sequentially and updates the workflow context with
    each step's output. It is intentionally simple so it can be extended with:
      - asynchronous execution
      - retries and error handling policies
      - persistence of workflow state
      - observability and tracing hooks
    """

    def __init__(self) -> None:
        self._running: Dict[str, Workflow] = {}

    def start(self, workflow: Workflow) -> None:
        """Start executing a workflow synchronously.

        Raises an exception if a workflow with the same id is already running.
        """
        if workflow.id in self._running:
            raise RuntimeError(f"Workflow {workflow.id} is already running")
        logger.debug("Starting workflow %s", workflow.id)
        self._running[workflow.id] = workflow
        try:
            self._execute(workflow)
        finally:
            # remove from running on completion
            self._running.pop(workflow.id, None)
            logger.debug("Workflow %s finished", workflow.id)

    def _execute(self, workflow: Workflow) -> None:
        for step in workflow.steps:
            logger.debug("Executing step %s (%s)", step.id, step.name)
            try:
                output = step.action(workflow.context)
                if output:
                    # merge output into context
                    workflow.context.update(output)
                logger.debug("Step %s completed. Context keys: %s", step.id, list(workflow.context.keys()))
            except Exception as exc:  # pragma: no cover - keep engine robust
                logger.exception("Step %s failed: %s", step.id, exc)
                # Simple failure policy: stop on first error
                raise

    def stop(self, workflow_id: str) -> None:
        """Stop a running workflow (best-effort)."""
        if workflow_id in self._running:
            # For this simple engine we cannot interrupt synchronous execution.
            # In a real engine this would signal cancellation to a background task.
            logger.info("Request to stop workflow %s received, but engine cannot cancel running synchronous workflows", workflow_id)
        else:
            logger.debug("Stop requested for unknown workflow %s", workflow_id)


# Small helper to build steps from simple callables
def make_step(step_id: str, func: Callable[[Dict[str, Any]], Dict[str, Any]], name: Optional[str] = None, meta: Optional[Dict[str, Any]] = None) -> Step:
    return Step(id=step_id, action=func, name=name, meta=meta or {})


# Example no-op action used in tests or examples
def noop_action(context: Dict[str, Any]) -> Dict[str, Any]:
    logger.debug("noop_action called with context keys: %s", list(context.keys()))
    return {}
