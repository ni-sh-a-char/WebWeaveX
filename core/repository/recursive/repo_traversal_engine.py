from __future__ import annotations

import re


def traverse_repo(text: str):
    paths = sorted(set(re.findall(r"[A-Za-z0-9_./-]+", text or "")))
    return {"paths": paths[:5000]}

