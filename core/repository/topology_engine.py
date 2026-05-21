from __future__ import annotations

from typing import Dict, Any
import re


def build_topology(text: str) -> Dict[str, Any]:
    src = text or ""
    paths = sorted(set(re.findall(r"[A-Za-z0-9_./-]+/[A-Za-z0-9_./-]+", src)))
    modules = sorted(set([p for p in paths if p.endswith((".py", ".js", ".ts", ".dart", ".java", ".kt"))]))
    packages = sorted(set([p for p in paths if p.endswith(("package.json", "pyproject.toml", "pubspec.yaml", "Cargo.toml", "pom.xml", "build.gradle"))]))
    services = sorted(set([p.split('/')[0] for p in paths if '/' in p]))
    entrypoints = sorted(set([p for p in modules if p.endswith(("main.py", "app.py", "index.js", "main.dart", "Main.java", "main.kt"))]))
    boundaries = sorted(set([p.rsplit('/', 1)[0] for p in modules if '/' in p]))
    return {"modules": modules, "services": services, "packages": packages, "entrypoints": entrypoints, "boundaries": boundaries}
