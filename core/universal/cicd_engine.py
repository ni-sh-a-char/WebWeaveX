from __future__ import annotations
import re

def parse_cicd(text: str):
    src = text or ''
    providers = []
    if '.github/workflows' in src: providers.append('github_actions')
    if 'gitlab-ci' in src: providers.append('gitlab_ci')
    if 'jenkinsfile' in src.lower(): providers.append('jenkins')
    jobs = sorted(set(re.findall(r'\bjobs?:\s*([A-Za-z0-9_-]+)?', src, flags=re.I)))
    return {"providers": sorted(set(providers)), "jobs": [j for j in jobs if j]}
