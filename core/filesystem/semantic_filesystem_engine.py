from __future__ import annotations

from typing import Dict


class SemanticFilesystem:

    def __init__(self) -> None:

        self.files: Dict[
            str,
            str,
        ] = {}

    def write(
        self,
        path: str,
        content: str,
    ) -> None:

        self.files[path] = content

    def read(
        self,
        path: str,
    ) -> str:

        return self.files.get(
            path,
            "",
        )

    def list_paths(self):

        return sorted(
            self.files.keys()
        )
