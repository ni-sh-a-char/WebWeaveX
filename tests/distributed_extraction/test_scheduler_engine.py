from core.distributed_extraction.extraction_scheduler_engine import (
    schedule_extraction_runtime,
)


def test_schedule_extraction_runtime():
    tasks = [
        {"task_id": "a", "url": "https://a.com", "priority": 2},
        {"task_id": "b", "url": "https://b.com", "priority": 1},
    ]

    result = schedule_extraction_runtime(tasks, tick=0)

    assert len(result["scheduled"]) == 2
    assert result["scheduled"][0]["run_at"] <= result["scheduled"][1]["run_at"]
