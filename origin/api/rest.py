from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/causal")

# -----------------------------
# 1) Causal Explain
# -----------------------------
class ExplainRequest(BaseModel):
    question: str

@router.post("/explain")
def explain(req: ExplainRequest):
    return {
        "target": "example_target",
        "parents": [
            {"factor": "supply_chain_delay", "weight": 0.85},
            {"factor": "labor_shortage", "weight": 0.62},
        ],
        "explanation": "This is a placeholder explanation from ORIGIN backend."
    }

# -----------------------------
# 2) What-If Simulation
# -----------------------------
class WhatIfRequest(BaseModel):
    variable: str
    new_value: float
    context: dict | None = None

@router.post("/what-if")
def what_if(req: WhatIfRequest):
    return {
        "variable": req.variable,
        "old_value": 1.0,
        "new_value": req.new_value,
        "estimated_effect": req.new_value - 1.0,
        "confidence_interval": [0.1, 0.9]
    }

# -----------------------------
# 3) DAG
# -----------------------------
@router.get("/dag")
def dag():
    return {
        "nodes": ["GDP", "interest_rate", "inflation", "port_performance"],
        "edges": [
            ["interest_rate", "GDP"],
            ["inflation", "GDP"],
            ["supply_chain_delay", "port_performance"]
        ]
    }

# -----------------------------
# 4) Policy Heatmap
# -----------------------------
class HeatmapRequest(BaseModel):
    var_x: str
    var_y: str

@router.post("/policy-heatmap")
def heatmap(req: HeatmapRequest):
    return {
        "x_values": [1, 2, 3, 4],
        "y_values": [10, 20, 30],
        "grid": [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9],
            [1.0, 1.1, 1.2]
        ]
    }
