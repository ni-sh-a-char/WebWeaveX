from core.memory import run_runtime_memory


def test_lineage_consistency():
    result = run_runtime_memory(tick=3)
    replay = result["replay"]

    first_lineage = list(replay["lineage"])
    second_lineage = list(replay["lineage"])

    assert first_lineage == second_lineage
    assert replay["memory_id"] == result["runtime"]["memory_id"]
