from core.distributed import schedule_distributed_execution


def test_scheduler():
    result = schedule_distributed_execution(
        tasks=[{"id": "t1"}],
        nodes=["a", "b"],
    )

    assert result["deterministic"] is True
