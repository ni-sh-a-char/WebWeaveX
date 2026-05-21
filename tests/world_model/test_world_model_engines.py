from core.world_model import (
    build_cross_file_dependencies,
    build_repository_knowledge_graph,
    build_semantic_ownership_graph,
    build_semantic_temporal_lineage,
    compress_semantic_context,
    forecast_semantic_execution,
    semantic_repository_search,
    suggest_semantic_refactor,
    track_semantic_evolution,
    traverse_repository_world,
)
from core.world_model.repository_semantic_memory_engine import (
    RepositorySemanticMemory,
)


def test_cross_file_dependencies():
    irs = [
        {"path": "a.py", "semantic_ast": {"imports": [{"module": "b.py"}]}},
        {"path": "b.py", "semantic_ast": {"imports": []}},
    ]
    result = build_cross_file_dependencies(irs)
    assert len(result["edges"]) == 1


def test_ownership_graph():
    irs = [
        {
            "path": "a.py",
            "semantic_ast": {"symbols": [{"name": "foo"}]},
        }
    ]
    result = build_semantic_ownership_graph(irs)
    assert result["ownership"]["foo"] == "a.py"


def test_execution_forecast():
    topology = {"nodes": [{"id": "b.py"}, {"id": "a.py"}]}
    result = forecast_semantic_execution(topology)
    assert result["forecast_order"] == ["a.py", "b.py"]


def test_semantic_memory():
    memory = RepositorySemanticMemory()
    memory.store("a.py", {"symbols": 1})
    assert memory.retrieve("a.py") == {"symbols": 1}


def test_evolution_tracker():
    result = track_semantic_evolution([{"v": 1}, {"v": 2}])
    assert result["depth"] == 2


def test_refactor_engine():
    ir = {
        "semantic_ast": {
            "symbols": [
                {"name": "dup"},
                {"name": "dup"},
            ]
        }
    }
    result = suggest_semantic_refactor(ir)
    assert result["refactor_required"] is True


def test_semantic_search():
    irs = [{"path": "src/main.py", "semantic_ast": {}}]
    result = semantic_repository_search("main", irs)
    assert result["count"] == 1


def test_temporal_lineage():
    result = build_semantic_temporal_lineage([{"state": 1}])
    assert len(result["timeline"]) == 1


def test_knowledge_graph():
    irs = [
        {
            "path": "a.py",
            "semantic_ast": {"symbols": [{"name": "run"}]},
        }
    ]
    result = build_repository_knowledge_graph(irs)
    assert result["entities"][0]["id"] == "run"


def test_repository_traversal():
    graph = {
        "edges": [
            {"from": "a.py", "to": "b.py"},
            {"from": "b.py", "to": "c.py"},
        ]
    }
    result = traverse_repository_world(graph, "a.py")
    assert result["visited"] == ["a.py", "b.py", "c.py"]


def test_context_compression():
    state = {f"k{i}": i for i in range(300)}
    result = compress_semantic_context(state)
    assert len(result["compressed"]) == 256
