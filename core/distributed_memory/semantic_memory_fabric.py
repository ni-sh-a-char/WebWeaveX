from __future__ import annotations

from typing import Any
from typing import Dict


class SemanticMemoryFabric:

    def __init__(self) -> None:

        self.regions: Dict[
            str,
            Dict[str, Any]
        ] = {}

    def put(
        self,
        region: str,
        key: str,
        value: Any,
    ) -> None:

        self.regions.setdefault(
            region,
            {},
        )

        self.regions[
            region
        ][key] = value

    def get(
        self,
        region: str,
        key: str,
    ) -> Any:

        return (
            self.regions
            .get(region, {})
            .get(key)
        )
