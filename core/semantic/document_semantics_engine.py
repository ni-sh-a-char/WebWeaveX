from __future__ import annotations

import re
from typing import Any, Dict, List


DOC_KIND_RULES = [
    ("contract", re.compile(r"agreement|terms|party|signature", re.I)),
    ("technical_doc", re.compile(r"architecture|module|implementation", re.I)),
    ("api_reference", re.compile(r"endpoint|request|response|openapi", re.I)),
    ("invoice", re.compile(r"invoice|amount due|tax", re.I)),
    ("report", re.compile(r"summary|findings|quarter|annual", re.I)),
    ("resume", re.compile(r"experience|education|skills", re.I)),
    ("legal", re.compile(r"whereas|jurisdiction|liability", re.I)),
    ("specification", re.compile(r"requirements|shall|must|specification", re.I)),
]


def extract_document_semantics(
    text: str = "",
) -> Dict[str, Any]:
    kinds = [kind for kind, pattern in DOC_KIND_RULES if pattern.search(text)]
    if not kinds:
        kinds = ["document"]

    return {
        "kinds": sorted(kinds),
        "primary_kind": sorted(kinds)[0],
        "length": len(text),
        "bounded": True,
    }
