#!/usr/bin/env python3
"""Runtime call trace of compile_document — which modules/functions actually EXECUTE,
and is any BeautifulSoup code path reached during compile_document(text)?"""
from __future__ import annotations
import sys, json

# Import WITH bs4 present (it is installed) so we can observe runtime behaviour.
from core.ir.document_ir import compile_document_ir

executed_modules = set()
executed_funcs = set()
bs4_hits = []
SUSPECT = ("table_semantics_engine", "ui_semantics_engine", "semantic_orchestrator")


def tracer(frame, event, arg):
    if event != "call":
        return
    code = frame.f_code
    mod = frame.f_globals.get("__name__", "?")
    fn = code.co_name
    fpath = code.co_filename.replace("\\", "/")
    if "/core/" in fpath or mod.startswith("core."):
        executed_modules.add(mod)
        executed_funcs.add(f"{mod}.{fn}")
        if "bs4" in fpath or any(s in fpath for s in SUSPECT) or "bs4" in mod:
            bs4_hits.append(f"{mod}.{fn}  ({fpath})")
    elif "bs4" in fpath or "beautifulsoup" in fpath.lower():
        bs4_hits.append(f"{mod}.{fn}  ({fpath})")
    return tracer


SAMPLES = [
    "",
    "# Title\nIntro paragraph.\n## Step 1\nDo the thing.\n## Step 2\nDo the next thing.\n",
    "1. first\n2. second\n3. third\n",
    "Therefore X. However Y. Because Z [1]. See reference [2].\n",
]

sys.setprofile(tracer)
outputs = [compile_document_ir(s) for s in SAMPLES]
sys.setprofile(None)

core_semantic_executed = sorted(m for m in executed_modules if m.startswith("core.semantic"))
result = {
    "executed_module_count": len(executed_modules),
    "executed_function_count": len(executed_funcs),
    "executed_modules": sorted(executed_modules),
    "core_semantic_modules_executed": core_semantic_executed,
    "bs4_or_suspect_calls_executed": bs4_hits,
    "behaviorally_reaches_bs4": len(bs4_hits) > 0,
    "sample_output_keys": sorted(outputs[1].keys()),
}
with open("_runtime_trace.json", "w", encoding="utf-8", newline="\n") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)
sys.stderr.write(
    f"executed core.* modules={len(executed_modules)} funcs={len(executed_funcs)}; "
    f"core.semantic executed={len(core_semantic_executed)}; "
    f"bs4/suspect call-hits={len(bs4_hits)} -> behaviorally_reaches_bs4={len(bs4_hits) > 0}\n")
for m in core_semantic_executed:
    sys.stderr.write(f"  core.semantic executed: {m}\n")
for h in bs4_hits[:10]:
    sys.stderr.write(f"  BS4-HIT: {h}\n")
