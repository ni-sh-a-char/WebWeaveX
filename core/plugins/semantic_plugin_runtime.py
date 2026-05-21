from __future__ import annotations

from typing import Any, Dict


class SemanticPluginRuntime:
    def __init__(self) -> None:
        self._plugins: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        metadata: Dict[str, Any],
    ) -> None:

        self._plugins[name] = metadata

    def list_plugins(self) -> Dict[str, Any]:
        return {
            "plugins": sorted(self._plugins.keys()),
        }
