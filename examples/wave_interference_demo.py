"""Wave propagation and interference demo."""

from origin.core.wave_engine import WaveEngine
from origin.graph.causal_graph import CausalGraph


def run() -> list[str]:
    graph = CausalGraph()
    graph.add_edge("smoking", "inflammation", 0.8, "causes")
    graph.add_edge("medication", "inflammation", 0.8, "treats")
    engine = WaveEngine()
    return [f"{result.node_id}: {result.mode}" for result in engine.interfere(engine.propagate(graph, "smoking"))]


if __name__ == "__main__":
    print(run())
