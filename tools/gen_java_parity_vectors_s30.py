#!/usr/bin/env python3
"""Session-30 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s30.py <out.json>

Covers the 3 PORT-APPROVED aggregators (JAVA_PENDING_API_AUDIT):
  - RuntimeKernel.run_pipeline   (canonical kernel; routes to 5 certified runtimes)
  - get_runtime_kernel           (singleton; certified via run_pipeline projection)
  - run_autonomous_extraction    (pure distributed scheduler; portable flag contract)

Python is the oracle. Every kernel vector uses a FRESH RuntimeKernel (run_pipeline mutates
instance state); every input keeps html="" (sources without runtime.html) so the semantic phase
stays on the certified html="" contract.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

import core.kernel.runtime_kernel as rk
from core.kernel import RuntimeKernel, get_runtime_kernel
from webweavex import run_autonomous_extraction


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def kernel_run(runtime_type, sources, tick, phases=None, options=None):
    k = RuntimeKernel(runtime_type=runtime_type)
    return k.run_pipeline(sources=sources, tick=tick, phases=phases, options=options)


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 30: kernel + autonomous aggregators)"}

    # ---- RuntimeKernel.run_pipeline ----
    out["RuntimeKernel"] = [
        ev("default_browser", {"runtime_type": "browser", "sources": {}, "tick": 0},
           kernel_run("browser", {}, 0)),
        ev("tick3", {"runtime_type": "browser", "sources": {}, "tick": 3},
           kernel_run("browser", {}, 3)),
        ev("repository_rt", {"runtime_type": "repository", "sources": {}, "tick": 0},
           kernel_run("repository", {}, 0)),
        ev("phases_subset", {"runtime_type": "browser", "sources": {}, "tick": 0,
                             "phases": ["semantic", "memory"]},
           kernel_run("browser", {}, 0, phases=["semantic", "memory"])),
        ev("opts_disable_semantic", {"runtime_type": "browser", "sources": {}, "tick": 0,
                                     "options": {"semantic": False}},
           kernel_run("browser", {}, 0, options={"semantic": False})),
    ]

    # ---- get_runtime_kernel: projection parity (fresh singleton → run_pipeline == fresh kernel) ----
    rk._KERNEL = None
    g = get_runtime_kernel("browser")
    out["get_runtime_kernel"] = [
        ev("projection_browser", {"runtime_type": "browser", "sources": {}, "tick": 0},
           g.run_pipeline(sources={}, tick=0)),
    ]

    # ---- run_autonomous_extraction (portable flag contract; native_extraction excluded) ----
    TASKS = [
        {"task_id": "t1", "url": "https://a", "priority": 0, "objective": "monitor_metrics"},
        {"task_id": "t2", "url": "https://b", "priority": 1},
        {"task_id": "t3", "url": "https://c", "priority": 0, "objective": "extract_dashboard"},
    ]
    out["run_autonomous_extraction"] = [
        ev("tasks", {"tasks": TASKS}, run_autonomous_extraction(tasks=TASKS)),
        ev("empty", {"tasks": []}, run_autonomous_extraction(tasks=[])),
        ev("workers", {"tasks": TASKS, "workers": [{"worker_id": "w1"}, {"worker_id": "w2"}]},
           run_autonomous_extraction(tasks=TASKS, workers=[{"worker_id": "w1"}, {"worker_id": "w2"}])),
        ev("tick", {"tasks": TASKS, "tick": 5}, run_autonomous_extraction(tasks=TASKS, tick=5)),
        ev("objective_exec", {"tasks": TASKS, "objective_execution": True},
           run_autonomous_extraction(tasks=TASKS, objective_execution=True)),
    ]

    path = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s30.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors)")


if __name__ == "__main__":
    main()
