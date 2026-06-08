#!/usr/bin/env python3
"""Run full Python→JS and Python→Dart ports + forensic audit."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT).returncode


def snapshot_protected() -> None:
    import shutil

    src = ROOT / "src"
    prot = ROOT / "tools" / "convergence" / "protected_js.txt"
    backup = ROOT / "tools" / "convergence" / "protected_backup"
    if not src.exists():
        return
    if backup.exists():
        shutil.rmtree(backup)
    lines: list[str] = []
    for p in sorted(src.rglob("*.ts")):
        if not p.is_file():
            continue
        rel = f"src/{p.relative_to(src).as_posix()}"
        lines.append(rel)
        dest = backup / p.relative_to(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    prot.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Protected {len(lines)} modules (backed up) -> {prot}")


def main() -> int:
    snapshot_protected()
    # Point py2ts at protected list
    prot_src = ROOT / "tools" / "py2ts" / "protected.txt"
    prot_dst = ROOT / "tools" / "convergence" / "protected_js.txt"
    if prot_dst.exists():
        prot_src.write_text(prot_dst.read_text(encoding="utf-8"), encoding="utf-8")

    code = run([sys.executable, str(ROOT / "tools" / "py2ts" / "py2ts.py")])
    if code != 0:
        return code
    code = run([sys.executable, str(ROOT / "tools" / "convergence" / "py2dart.py")])
    if code != 0:
        return code
    return run([sys.executable, str(ROOT / "tools" / "convergence" / "forensic_audit.py")])


if __name__ == "__main__":
    sys.exit(main())
