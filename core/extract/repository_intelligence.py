from __future__ import annotations

import re
from collections import Counter
from typing import Dict, Any


def extract_repository_intelligence(text: str, source_url: str = "") -> Dict[str, Any]:
    src = text or ""
    files = sorted(set(re.findall(r"[A-Za-z0-9_./-]+\.(?:py|js|ts|tsx|md|json|yml|yaml|toml|go|rs|java|kt|php)", src)))
    ext_counter = Counter([f.rsplit('.', 1)[-1].lower() for f in files])
    languages = {k: ext_counter[k] for k in sorted(ext_counter.keys())}
    packages = sorted(set(re.findall(r"(?:package|module|service)\s+([A-Za-z0-9_./-]+)", src, flags=re.IGNORECASE)))
    imports = sorted(set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z0-9_.-]+)", src, flags=re.MULTILINE)))
    configs = sorted(set(re.findall(r"(?:^|\s)(?:package\.json|pyproject\.toml|requirements\.txt|Dockerfile|docker-compose\.yml|tsconfig\.json)", src, flags=re.IGNORECASE)))
    readme_headers = sorted(set(re.findall(r"^#{1,6}\s+(.+)$", src, flags=re.MULTILINE)))
    api_routes = sorted(set(re.findall(r"(?:GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9_\-/{}/:]+)", src)))

    return {
        "repository_intelligence": {
            "source_url": source_url,
            "repository_tree": files[:1000],
            "language_distribution": languages,
            "package_boundaries": packages[:500],
            "dependency_graph": {"imports": imports[:2000]},
            "service_module_relationships": sorted(set([p.split('/')[0] for p in packages if p])),
            "readme_source_alignment": {"readme_sections": readme_headers[:200], "code_file_count": len(files)},
            "framework_detection": sorted(set(re.findall(r"(next\.js|react|django|flask|fastapi|spring|laravel|express|nestjs)", src, flags=re.IGNORECASE))),
            "configuration_relationships": configs,
            "api_route_structure": api_routes,
            "monorepo_package_mapping": sorted(set(re.findall(r"packages/[A-Za-z0-9_.-]+", src))),
        }
    }
