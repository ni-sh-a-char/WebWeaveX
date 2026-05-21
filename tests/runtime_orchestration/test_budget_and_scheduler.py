from core.runtime.runtime_budget_engine import DEFAULT_RUNTIME_BUDGET
from core.runtime.semantic_scheduler_engine import schedule_semantic_runtime_tasks


def test_scheduler_respects_task_budget():
    tasks = [{"id": str(i), "priority": i} for i in range(DEFAULT_RUNTIME_BUDGET.max_tasks + 10)]
    r = schedule_semantic_runtime_tasks(tasks)
    assert len(r["scheduled"]) == DEFAULT_RUNTIME_BUDGET.max_tasks
    assert r["dropped"] == 10
