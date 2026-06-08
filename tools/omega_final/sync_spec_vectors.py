#!/usr/bin/env python3
"""Copy validation/vectors to specification/vectors with webweavex-spec authority tag."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "validation/vectors"
DST = ROOT / "specification/vectors"


def main() -> int:
    if not SRC.exists():
        print("No validation/vectors to sync")
        return 1
    DST.mkdir(parents=True, exist_ok=True)
    n = 0
    for canonical in SRC.glob("*/canonical.json"):
        family = canonical.parent.name
        target_dir = DST / family
        target_dir.mkdir(parents=True, exist_ok=True)
        data = json.loads(canonical.read_text(encoding="utf-8"))
        data["source"] = "webweavex-spec"
        data["spec_synced_at"] = datetime.now(timezone.utc).isoformat()
        if data.get("source_note"):
            del data["source_note"]
        (target_dir / "canonical.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        n += 1
    manifest = ROOT / "specification/vectors/manifest.json"
    if manifest.exists():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        m["families_synced"] = n
        m["synced_at"] = datetime.now(timezone.utc).isoformat()
        manifest.write_text(json.dumps(m, indent=2), encoding="utf-8")
    print(f"Synced {n} vector families to specification/vectors/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
