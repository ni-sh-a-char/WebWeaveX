from __future__ import annotations

from typing import Any, Dict


MAX_COMPRESSED_KEYS = 256


def compress_semantic_repository(
    repository: Dict[str, Any],
) -> Dict[str, Any]:
    keys = sorted(repository.keys())[:MAX_COMPRESSED_KEYS]
    return {
        "compressed": {
            key: repository[key]
            for key in keys
        },
        "compression_ratio": round(
            len(keys) / max(len(repository), 1),
            3,
        ),
    }
