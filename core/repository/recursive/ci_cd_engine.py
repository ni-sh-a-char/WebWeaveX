from __future__ import annotations

import re


def extract_ci_cd(text: str):
    src = text or ""
    pipelines = sorted(set(re.findall(r"(?:\.github/workflows/\S+|gitlab-ci\.yml|Jenkinsfile)", src, flags=re.IGNORECASE)))
    deployments = sorted(set(re.findall(r"(?:kubernetes|k8s|helm|deploy)\S*", src, flags=re.IGNORECASE)))
    containers = sorted(set(re.findall(r"(?:Dockerfile|docker-compose\.(?:yml|yaml))", src, flags=re.IGNORECASE)))
    infra = sorted(set(re.findall(r"(?:terraform|\.tf\b)", src, flags=re.IGNORECASE)))
    return {"pipelines": pipelines, "deployments": deployments, "containers": containers, "infra": infra}

