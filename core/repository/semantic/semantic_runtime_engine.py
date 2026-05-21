from __future__ import annotations

from typing import Dict, List


def detect_semantic_runtime(dependencies: List[str], build_files: List[str], configs: List[str]) -> Dict[str, List[str]]:
    deps = {d.lower() for d in dependencies or []}
    files = {f.lower() for f in build_files or []}
    cfgs = {c.lower() for c in configs or []}

    runtimes = set()
    if {"django", "flask", "fastapi", "uvicorn"} & deps or "requirements.txt" in files:
        runtimes.add("python")
    if {"react", "next", "express", "nestjs"} & deps or "package.json" in files:
        runtimes.add("node")
    if "pom.xml" in files or "build.gradle" in files:
        runtimes.add("jvm")
    if "pubspec.yaml" in files:
        runtimes.add("dart")
    if "cargo.toml" in files:
        runtimes.add("rust")
    if "go.mod" in files:
        runtimes.add("go")

    orchestration = sorted([x for x in cfgs if x.endswith((".yml", ".yaml", ".tf", "dockerfile"))])
    return {"runtimes": sorted(runtimes), "orchestration_configs": orchestration}
