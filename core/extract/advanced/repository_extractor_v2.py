from __future__ import annotations

from typing import Dict, Any
import re


def extract_repository_v2(text: str) -> Dict[str, Any]:
    src = text or ""
    files = sorted(set(re.findall(r"[A-Za-z0-9_./-]+", src)))
    ci = sorted(set([f for f in files if f.endswith((".yml", ".yaml")) and (".github/workflows" in f or "gitlab-ci" in f or "bitbucket-pipelines" in f)]))
    containers = sorted(set([f for f in files if f in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml") or f.endswith("Dockerfile")]))
    infra = sorted(set([f for f in files if any(x in f for x in ["terraform", "helm", "k8s", "kubernetes"]) ]))
    configs = sorted(set([f for f in files if f.endswith((".json", ".toml", ".yaml", ".yml", ".ini", ".cfg"))]))
    entrypoints = sorted(set([f for f in files if f.endswith(("main.py", "app.py", "index.js", "main.dart", "Main.java"))]))
    return {"repository_structure": files[:2000], "entrypoints": entrypoints, "ci_cd_files": ci, "infra_files": infra, "container_files": containers, "config_files": configs}
