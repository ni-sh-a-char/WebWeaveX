from core.semantic import run_semantic_runtime
from core.semantic.ontology_engine import build_semantic_ontology
from core.semantic.semantic_replay_engine import replay_semantic_runtime


def test_semantic_replay_identical():
    result = run_semantic_runtime(
        url="https://example.com/dashboard",
        html="<form><button>Login</button></form>",
        objective="extract_dashboard",
    )

    memory = result["memory"]
    first = replay_semantic_runtime(memory)
    second = replay_semantic_runtime(memory)

    assert first == second
    assert result["replay"] == first


def test_ontology_consistency():
    entities = [{"id": "e1", "type": "api", "label": "api"}]
    first = build_semantic_ontology(entities, "developer_tooling")
    second = build_semantic_ontology(entities, "developer_tooling")

    assert first == second
