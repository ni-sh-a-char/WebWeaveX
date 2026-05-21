from core.distributed_extraction import run_autonomous_extraction


def test_autonomous_extraction():
    result = run_autonomous_extraction(
        tasks=[{"task_id": "t1", "url": "https://example.com", "priority": 1}],
        tick=0,
    )

    assert result["autonomous"] is True
    assert result["workers"]
    assert result["checkpoint"]["bounded"] is True
