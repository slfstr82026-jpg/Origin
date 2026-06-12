from origin.graph.model import NodeSchema, EdgeSchema


def test_node_and_edge_schema_basic():
    n = NodeSchema(id="glucose", type="metabolite", metadata={"unit": "mmol/L"})
    assert n.id == "glucose"
    e = EdgeSchema(source="insulin", target="glucose", weight=0.8, phase=0.0)
    assert e.source == "insulin"
    assert e.weight == 0.8
