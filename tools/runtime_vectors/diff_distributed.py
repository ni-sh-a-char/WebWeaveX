#!/usr/bin/env python3
"""Compare Python vs JS distributed extraction stable serialization."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/runtime_vectors/.py_staging"))

from core.distributed_extraction.distributed_extraction_orchestrator import run_distributed_extraction
from core.determinism.normalization import stable_serialize

tasks = [{"task_id": "t1", "url": "https://example.com", "priority": 2}]
py_out = run_distributed_extraction(tasks, None, {}, 0, [])
py_s = stable_serialize(py_out)

js = subprocess.run(
    [
        "npx",
        "tsx",
        "-e",
        """
import { runDistributedExtraction } from './src/distributed/distributedExtractionOrchestrator.js';
import { stableSerialize } from './src/determinism/normalization.js';
const out = runDistributedExtraction([{task_id:'t1',url:'https://example.com',priority:2}], undefined, {}, 0, []);
console.log(stableSerialize(out));
""",
    ],
    cwd=ROOT,
    capture_output=True,
    text=True,
    encoding="utf-8",
)
js_s = js.stdout.strip()

print("py len", len(py_s), "js len", len(js_s))
if py_s == js_s:
    print("MATCH")
else:
    for i, (a, b) in enumerate(zip(py_s, js_s)):
        if a != b:
            print("first diff at", i, repr(py_s[max(0, i - 20) : i + 40]))
            print("py", repr(py_s[i : i + 80]))
            print("js", repr(js_s[i : i + 80]))
            break
