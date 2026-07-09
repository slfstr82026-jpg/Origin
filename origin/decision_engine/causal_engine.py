import asyncio
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

# Setup structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ORIGIN_Causal_Engine")

# 1. Define the Strict Output Schema for the Causal Decision
class CausalDecisionSchema(BaseModel):
    root_cause: str = Field(description="The identified ultimate root cause of the incident.")
    confidence_score: float = Field(description="Confidence metrics from 0.0 to 1.0 based on data availability.")
    recommended_action: str = Field(description="The primary operational decision to execute immediately.")
    mitigation_strategy: str = Field(description="Fallback strategy if the primary action fails.")
    impact_analysis: Dict[str, str] = Field(description="Key-value mapping of causal impacts across sectors.")

# 2. Define the State Graph Shared Memory
class EngineState(TypedDict):
    incident_description: str
    api_responses: Dict[str, Any]
    final_decision: Optional[CausalDecisionSchema]
    errors: List[str]

# 3. Simulate Parallel APIs with Built-in Fallbacks & Circuit Breaking
async def fetch_api_data(api_name: str, payload: str, simulate_fail: bool = False) -> Dict[str, Any]:
    """
    Simulates high-throughput API calls with strict timeouts and safe fallback injection.
    """
    try:
        if simulate_fail:
            # Simulate a cascade failure or rate-limiting error
            raise asyncio.TimeoutError(f"Gateway Timeout on downstream dependency: {api_name}")
        
        logger.info(f"Initiating parallel burst request to: {api_name}")
        await asyncio.sleep(0.4) # Simulating I/O Latency
        return {"status": "success", "data": f"Validated real-time metrics from {api_name}"}
        
    except Exception as e:
        logger.error(f"Circuit Breaker Triggered for {api_name}. Error: {str(e)}")
        # Self-healing Injection: Return stale or baseline deterministic data instead of failing
        return {"status": "fallback_degraded", "data": f"Degraded historical backup data for {api_name}"}

# 4. Define LangGraph Nodes (State Transformers)
async def ingest_incident_node(state: EngineState) -> Dict[str, Any]:
    logger.info("Node 1: Parsing unstructured incident telemetry data.")
    return {"errors": [], "api_responses": {}}

async def parallel_tool_execution_node(state: EngineState) -> Dict[str, Any]:
    logger.info("Node 2: Executing concurrent asynchronous tool execution with fault isolation.")
    incident = state["incident_description"]
    
    # Fire off concurrent tasks. Simulating API_2 failure to demonstrate resiliency
    tasks = [
        fetch_api_data("Infrastructure_IoT_API", incident, simulate_fail=False),
        fetch_api_data("Live_Demand_Telemetry_API", incident, simulate_fail=True), # This will gracefully fall back
        fetch_api_data("Dynamic_Risk_Engine_API", incident, simulate_fail=False)
    ]
    
    results = await asyncio.gather(*tasks)
    
    combined_responses = {
        "Infrastructure_IoT": results[0],
        "Live_Demand": results[1],
        "Dynamic_Risk": results[2]
    }
    
    captured_errors = [res["data"] for res in results if res["status"] == "fallback_degraded"]
    return {"api_responses": combined_responses, "errors": captured_errors}

async def causal_reasoning_node(state: EngineState) -> Dict[str, Any]:
    logger.info("Node 3: Invoking Causal Reasoner via Structured Output Constraint Layer.")
    
    # In a live production environment, this is where you pass the context to the LLM.
    # We enforce structured compilation using the Pydantic class via standard extraction frameworks.
    # Mocking LLM structured convergence under strict constraint:
    mock_llm_response = CausalDecisionSchema(
        root_cause="Concurrent downstream DB deadlock cascading into Redis Cache invalidation.",
        confidence_score=0.88 if not state["errors"] else 0.72, # Drop confidence if relying on fallbacks
        recommended_action="Isolate affected database shard, initiate automated replication failover loop.",
        mitigation_strategy="Apply hard rate-limiting on incoming edge gateways via Redis fallback cluster.",
        impact_analysis={"Financial": "Prevents double spending on 10k transactions", "System": "Maintains eventual consistency"}
    )
    
    return {"final_decision": mock_llm_response}

# 5. Graph Construction & Compilation
def compile_causal_engine() -> StateGraph:
    builder = StateGraph(EngineState)
    
    # Register Nodes
    builder.add_node("IngestIncident", ingest_incident_node)
    builder.add_node("ParallelTools", parallel_tool_execution_node)
    builder.add_node("CausalReasoning", causal_reasoning_node)
    
    # Establish State Directed Edges
    builder.set_entry_point("IngestIncident")
    builder.add_edge("IngestIncident", "ParallelTools")
    builder.add_edge("ParallelTools", "CausalReasoning")
    builder.add_edge("CausalReasoning", END)
    
    return builder.compile()

# 6. Test Suite Execution Block
if __name__ == "__main__":
    logger.info("Compiling ORIGIN Causal Workflow Engine Instance...")
    runtime_graph = compile_causal_engine()
    
    # Mocking Stress Test Case Scenario 10
    stress_payload = {
        "incident_description": "Database node failure coupled with absolute Redis cache connection termination during peak live checkout load."
    }
    
    logger.info("Injecting telemetry stream into active state execution machine...")
    output = asyncio.run(runtime_graph.ainvoke(stress_payload))
    
    print("\n" + "="*40 + " ENGINE OUTPUT DECISION " + "="*40)
    if output["final_decision"]:
        decision: CausalDecisionSchema = output["final_decision"]
        print(f"Root Cause Isolation : {decision.root_cause}")
        print(f"Confidence Metric    : {decision.confidence_score * 100}%")
        print(f"Primary Action Order : {decision.recommended_action}")
        print(f"Degraded Mitigator   : {decision.mitigation_strategy}")
        print(f"Faults Intercepted   : {output['errors']}")
    print("="*104)
