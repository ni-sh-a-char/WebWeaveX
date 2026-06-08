#!/usr/bin/env python3
"""Resumable, parallel certification matrix runner.

Certifies every Python⇄TypeScript module pair via executable probes, writing
incremental results to a JSONL checkpoint so interrupted runs resume cleanly.

Usage:
  python -B tools/convergence/matrix_runner.py [--workers 8] [--fresh] [--only-failed]

Output:
  docs/specs/matrix_checkpoint.jsonl   (one row per certified module, incremental)
  docs/specs/generated_module_matrix.json  (rebuilt at end of each run)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "docs/specs"
CHECKPOINT = SPECS / "matrix_checkpoint.jsonl"

sys.path.insert(0, str(ROOT / "tools/convergence"))
sys.path.insert(0, str(ROOT / "tools/py2ts"))


def certify_one(py_path: str) -> dict:
    # imported inside worker process
    sys.path.insert(0, str(ROOT / "tools/convergence"))
    sys.path.insert(0, str(ROOT / "tools/py2ts"))
    from module_certifier import certify_module
    from py2ts import py_path_to_ts

    ts_rel = "src/" + py_path_to_ts(py_path)
    # browser modules launch real Chromium via the sync bridge — allow startup
    heavy = "/browser/" in py_path or "playwright" in py_path
    try:
        return certify_module(py_path, ts_rel, timeout=240 if heavy else 45)
    except Exception as exc:  # noqa: BLE001
        return {
            "module": py_path,
            "python_module": py_path,
            "javascript_module": ts_rel,
            "status": "FAIL",
            "error": f"certifier_crash:{exc}",
            "python_executed": False,
            "javascript_executed": False,
            "output_match": False,
            "runtime_match": False,
            "semantic_match": False,
            "memory_match": False,
            "probe_function": None,
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--fresh", action="store_true", help="discard checkpoint")
    ap.add_argument("--only-failed", action="store_true", help="re-run only non-PASS checkpoint rows")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    print("Materializing Python staging...", flush=True)
    subprocess.run(
        [sys.executable, str(ROOT / "tools/runtime_vectors/materialize_python.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )

    # deterministic local HTTP endpoint for fetcher/crawler probes
    server_proc = None
    import socket

    with socket.socket() as s:
        if s.connect_ex(("127.0.0.1", 8787)) != 0:
            server_proc = subprocess.Popen(
                [sys.executable, "-B", str(ROOT / "tools/convergence/probe_http_server.py")],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("started probe http server on 8787", flush=True)

    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    manifest = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().endswith(".py")]

    done: dict[str, dict] = {}
    if args.fresh and CHECKPOINT.exists():
        CHECKPOINT.unlink()
    if CHECKPOINT.exists():
        for ln in CHECKPOINT.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                row = json.loads(ln)
                done[row["python_module"]] = row
            except json.JSONDecodeError:
                continue

    if args.only_failed:
        todo = [m for m in manifest if done.get(m, {}).get("status") != "PASS"]
        # drop stale rows for modules being re-run
        for m in todo:
            done.pop(m, None)
    else:
        todo = [m for m in manifest if m not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"manifest={len(manifest)} done={len(done)} todo={len(todo)} workers={args.workers}", flush=True)

    counts: dict[str, int] = {}
    for row in done.values():
        counts[row["status"]] = counts.get(row["status"], 0) + 1

    if todo:
        with CHECKPOINT.open("a", encoding="utf-8") as ckpt, ProcessPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(certify_one, m): m for m in todo}
            n = 0
            for fut in as_completed(futures):
                row = fut.result()
                done[row["python_module"]] = row
                ckpt.write(json.dumps(row, default=str) + "\n")
                ckpt.flush()
                counts[row["status"]] = counts.get(row["status"], 0) + 1
                n += 1
                if n % 50 == 0:
                    print(f"  {n}/{len(todo)}  {counts}", flush=True)

    # rebuild full matrix in manifest order
    ts = datetime.now(timezone.utc).isoformat()
    rows = [done[m] for m in manifest if m in done]
    payload = {"measured_at": ts, "modules": rows}
    (SPECS / "generated_module_matrix.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (ROOT / "docs/archive/generated_module_matrix.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    finals: dict[str, int] = {}
    for row in rows:
        finals[row["status"]] = finals.get(row["status"], 0) + 1
    print(f"MATRIX: total={len(rows)} {finals}", flush=True)
    if server_proc is not None:
        server_proc.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
