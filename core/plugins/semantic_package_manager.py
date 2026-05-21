from __future__ import annotations

from typing import List


class SemanticPackageManager:
    def __init__(self) -> None:
        self._packages: List[str] = []

    def install(
        self,
        package: str,
    ) -> None:

        if package not in self._packages:
            self._packages.append(package)

    def list_packages(self) -> List[str]:
        return sorted(self._packages)
