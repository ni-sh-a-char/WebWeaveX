from __future__ import annotations

from typing import Any, Dict

from core.distributed_extraction.distributed_checkpoint_engine import (
    load_distributed_checkpoint,
    save_distributed_checkpoint,
)


def persist_distributed_state(
    path: str,
    state: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    return save_distributed_checkpoint(path, state, key)


def restore_distributed_state(
    path: str,
    key: str,
) -> Dict[str, Any]:
    return load_distributed_checkpoint(path, key)
