from __future__ import annotations

from typing import Dict


def classify_repo(url: str) -> Dict[str, str]:
    u = (url or "").lower()
    if "github.com" in u:
        provider = "github"
    elif "gitlab" in u:
        provider = "gitlab"
    elif "bitbucket" in u:
        provider = "bitbucket"
    else:
        provider = "unknown"
    return {"provider": provider}
