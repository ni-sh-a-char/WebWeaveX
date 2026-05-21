from __future__ import annotations

from dataclasses import dataclass


MAX_RUNTIME_TASKS = 1000
MAX_RUNTIME_MEMORY_MB = 512
MAX_RUNTIME_SECONDS = 30


@dataclass(frozen=True)
class RuntimeBudget:
    max_tasks: int = MAX_RUNTIME_TASKS
    max_memory_mb: int = MAX_RUNTIME_MEMORY_MB
    max_runtime_seconds: int = MAX_RUNTIME_SECONDS


DEFAULT_RUNTIME_BUDGET = RuntimeBudget()
