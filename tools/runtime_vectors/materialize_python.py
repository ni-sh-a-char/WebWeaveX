#!/usr/bin/env python3
"""Materialize origin/python core/ into .py_staging for canonical probe execution."""
from __future__ import annotations

import subprocess
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGING = Path(__file__).resolve().parent / ".py_staging"
STAMP = STAGING / ".origin_python_ref"
ZIP_PATH = STAGING / "core.zip"


def origin_python_ref() -> str:
    r = subprocess.run(
        ["git", "rev-parse", "origin/python"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return r.stdout.strip()


def materialize(*, force: bool = False) -> Path:
    ref = origin_python_ref()
    if not force and STAMP.exists() and STAMP.read_text(encoding="utf-8") == ref and (STAGING / "core").is_dir():
        return STAGING

    STAGING.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "archive", "--format=zip", "origin/python", "core"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    ZIP_PATH.write_bytes(proc.stdout)
    if (STAGING / "core").exists():
        import shutil

        shutil.rmtree(STAGING / "core")
    with zipfile.ZipFile(BytesIO(proc.stdout)) as zf:
        zf.extractall(STAGING)
    # Strip UTF-8 BOM from extracted sources so AST probes parse reliably.
    for py_file in (STAGING / "core").rglob("*.py"):
        raw = py_file.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            py_file.write_bytes(raw[3:])
    STAMP.write_text(ref, encoding="utf-8")
    return STAGING


if __name__ == "__main__":
    path = materialize(force="--force" in __import__("sys").argv)
    print(f"materialized: {path / 'core'} ({STAMP.read_text(encoding='utf-8')[:12]}…)")
