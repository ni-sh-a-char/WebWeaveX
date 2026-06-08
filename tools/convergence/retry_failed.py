#!/usr/bin/env python3
"""Retry failed Python→TS conversions after BOM/import fixes."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "py2ts"))

from py2ts import (  # noqa: E402
    ModuleEmitter,
    git_show,
    load_manifest,
    postprocess,
    py_path_to_ts,
)

SRC = ROOT / "src"


def main() -> int:
    manifest = load_manifest()
    missing = []
    for py in manifest:
        ts = py_path_to_ts(py)
        if not (SRC / ts).exists():
            missing.append(py)
    ok = fail = 0
    for py in missing:
        src = git_show(py)
        if not src:
            fail += 1
            continue
        ts = py_path_to_ts(py)
        out = SRC / ts
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(postprocess(ModuleEmitter(py, ts).convert(src)), encoding="utf-8")
            ok += 1
        except Exception as ex:
            fail += 1
            print(f"FAIL {py}: {ex}")
    print(f"Retry: {ok} ok, {fail} still missing, total src={(len(list(SRC.rglob('*.ts'))))}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
