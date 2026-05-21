from __future__ import annotations

def detect_build_systems(text: str):
    src=(text or '').lower()
    out=[]
    for k,v in [('pyproject.toml','python'),('package.json','node'),('pom.xml','maven'),('build.gradle','gradle'),('cargo.toml','cargo')]:
        if k in src: out.append(v)
    return sorted(set(out))
