from __future__ import annotations

import hashlib
import json

from typing import Any, Dict


class SemanticCache:

    def __init__(self) -> None:

        self._cache: Dict[str, Any] = {}

    def _fingerprint(
        self,
        payload: Dict[str, Any],
    ) -> str:

        encoded = json.dumps(
            payload,
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            encoded.encode("utf-8")
        ).hexdigest()

    def put(
        self,
        payload: Dict[str, Any],
        value: Any,
    ) -> str:

        fp = self._fingerprint(
            payload,
        )

        self._cache[fp] = value

        return fp

    def get(
        self,
        payload: Dict[str, Any],
    ) -> Any:

        fp = self._fingerprint(
            payload,
        )

        return self._cache.get(fp)
