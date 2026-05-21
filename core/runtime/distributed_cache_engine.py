from __future__ import annotations

import hashlib
import json

from typing import Any
from typing import Dict


class DistributedSemanticCache:

    def __init__(self) -> None:

        self.cache: Dict[
            str,
            Dict[str, Any]
        ] = {}

    def put(
        self,
        payload: Dict[str, Any],
    ) -> str:

        raw = json.dumps(
            payload,
            sort_keys=True,
            default=str,
        )

        key = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

        self.cache[key] = payload

        return key

    def get(
        self,
        key: str,
    ) -> Dict[str, Any]:

        return self.cache.get(
            key,
            {},
        )
