from __future__ import annotations

from threading import Lock

from typing import Dict


LOCKS: Dict[str, Lock] = {}


def acquire_semantic_lock(
    key: str,
) -> bool:

    if key not in LOCKS:

        LOCKS[key] = Lock()

    return LOCKS[key].acquire(
        blocking=False,
    )


def release_semantic_lock(
    key: str,
) -> None:

    if key in LOCKS:

        try:
            LOCKS[key].release()

        except RuntimeError:
            pass
