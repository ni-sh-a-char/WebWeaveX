#!/usr/bin/env python3
"""Final enterprise validation — real metrics only."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
REPORT = ARCHIVE / "FINAL_ENTERPRISE_VALIDATION_REPORT.md"


def _hash(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:32]


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from core.browser.universal_web_extraction_engine import extract_web
    from core.contracts.runtime_contracts import UniversalInput
    from core.crypto.kaalka_runtime_engine import encrypt_value
    from core.kernel.runtime_pipeline import run_canonical_pipeline
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
    import webweavex

    rows = []

    t0 = time.perf_counter()
    ex = extract_web("https://example.com")
    rows.append(
        {
            "browser": True,
            "ms": round((time.perf_counter() - t0) * 1000, 2),
            "graph_hash": _hash(ex.get("unified_runtime_graph", {})),
            "dom_hash": ex.get("runtime", {}).get("dom_stabilization", {}).get("stabilized_hash"),
        }
    )

    t0 = time.perf_counter()
    g1 = extract_web("https://github.com")
    g2 = extract_web("https://github.com")
    ir1 = _hash(g1.get("browser_ir", {}))
    ir2 = _hash(g2.get("browser_ir", {}))
    rows.append(
        {
            "github_ir_stable": ir1 == ir2,
            "ms": round((time.perf_counter() - t0) * 1000, 2),
            "ir_hash": ir1,
        }
    )

    pipe = run_canonical_pipeline(
        UniversalInput(source="https://example.com", source_type="web"),
        options={
            "kernel": {
                "semantic": False,
                "sync": False,
                "memory": False,
                "execution": False,
                "reconstruction": False,
            }
        },
    )
    rows.append({"pipeline_hash": pipe.get("pipeline_hash")})

    enc = [encrypt_value("probe", "k")["encrypted"] for _ in range(3)]
    rows.append({"kaalka_stable": len(set(enc)) == 1})

    r = reconstruct_runtime(runtime_type="browser", tick=0)
    rows.append({"reconstruction_id": r["runtime_id"]})

    body = [
        "# FINAL ENTERPRISE VALIDATION REPORT",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"**Version:** {webweavex.__version__}",
        "",
        "```json",
        json.dumps(rows, indent=2),
        "```",
    ]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(body), encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
