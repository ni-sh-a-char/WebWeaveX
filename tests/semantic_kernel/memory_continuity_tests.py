from core.memory import SemanticMemory, evolve_semantic_state, track_continuity, diff_semantic_ir


def test_memory_bounded():
    m = SemanticMemory(max_entries=2)
    m.put("a", 1)
    m.put("b", 2)
    m.put("c", 3)
    assert m.snapshot()["count"] <= 2


def test_evolution_deterministic():
    e = evolve_semantic_state({"version": 1, "x": 1}, {"version": 1, "x": 2})
    assert e["version"] == 2
    assert e["changes"]["has_changes"] is True


def test_continuity():
    c = track_continuity({"a": 1}, {"a": 2, "b": 3})
    assert "a" in c["continuous_keys"] or c["continuous"]
