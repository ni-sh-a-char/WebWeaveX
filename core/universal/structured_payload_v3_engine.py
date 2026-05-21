from __future__ import annotations
import re

def parse_structured_payload(text: str):
    src = text or ''
    return {
        "has_openapi": bool(re.search(r'openapi\s*:\s*3', src, flags=re.I)),
        "has_graphql": 'type Query' in src or 'schema {' in src,
        "has_dockerfile": 'FROM ' in src,
        "has_ci": any(k in src for k in ['github/workflows', 'gitlab-ci', 'Jenkinsfile']),
    }
