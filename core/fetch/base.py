from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict
import hashlib


@dataclass(frozen=True)
class FetchResponse:
    source: str
    url: str
    status_code: int
    content_type: str
    text: str
    ok: bool
    error: str
    metadata: Dict[str, str]

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["metadata"] = dict(sorted((self.metadata or {}).items()))
        data["fingerprint"] = hashlib.sha256(
            f"{self.source}|{self.url}|{self.status_code}|{self.content_type}|{self.text}".encode("utf-8", errors="ignore")
        ).hexdigest()
        return data

