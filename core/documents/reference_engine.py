from __future__ import annotations

import re
from typing import Any, Dict


def extract_references(text: str) -> Dict[str, Any]:
    src = text or ""
    external = sorted(set(re.findall(r"""https?://[^\s\)\]'""]+""", src)))
    internal = sorted(set(re.findall(r"\[[^\]]+\]\((/[^)]+)\)", src)))
    repo_refs = sorted(set([u for u in external if any(x in u for x in ["github.com", "gitlab", "bitbucket"])]))
    pkg_refs = sorted(set([u for u in external if any(x in u for x in ["pypi.org", "npmjs.com", "pub.dev"])]))
    return {
        "internal_links": internal,
        "external_links": external,
        "citations": external,
        "repo_references": repo_refs,
        "package_references": pkg_refs,
    }

