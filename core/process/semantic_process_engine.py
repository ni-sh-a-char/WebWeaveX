from __future__ import annotations

from dataclasses import dataclass

from typing import Dict
from typing import Any
from typing import List


@dataclass
class SemanticProcess:

    pid: int

    state: str

    memory: Dict[str, Any]

    tasks: List[Dict[str, Any]]


MAX_PROCESSES = 1000


class SemanticProcessTable:

    def __init__(self) -> None:

        self.processes: Dict[
            int,
            SemanticProcess,
        ] = {}

    def register(
        self,
        process: SemanticProcess,
    ) -> None:

        if len(self.processes) >= MAX_PROCESSES:
            return

        self.processes[
            process.pid
        ] = process

    def snapshot(self) -> Dict[str, Any]:

        return {
            "count": len(
                self.processes
            ),
            "pids": sorted(
                self.processes.keys()
            ),
        }
