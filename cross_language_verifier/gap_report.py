"""Generate dart_extraction_gap_report.json: every Python public API missing in
Dart, with module, signature, AST import closure, size estimate, and blocking
status — recomputed from source."""
import ast
import inspect
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
import webweavex as w

PY_ROOT = Path(r"C:\Projects\wwx_cert_py")

MISSING = [
    "capture_dom_mutations", "capture_websocket_frames", "crawl", "crawl_async",
    "extract", "extract_async", "extract_docs", "extract_document_runtime",
    "extract_infinite_scroll", "extract_multimodal", "extract_native",
    "extract_paginated_content", "extract_recursive", "extract_repo",
    "extract_repository", "ingest_input", "recover_modal_runtime",
    "run_application_cognition", "run_autonomous_extraction",
    "run_native_cognition", "stream_extract", "universal_extract",
    "run_live_runtime",
]

PLATFORM_MARKERS = {
    "playwright": "live browser page required",
    "sys.platform": "OS-coupled native runtime",
    "subprocess": "OS process execution",
    "psutil": "OS process inspection",
}
NETWORK_MARKERS = {"requests": "HTTP fetch", "httpx": "HTTP fetch", "urllib.request": "HTTP fetch"}


def module_of(fn):
    try:
        return Path(inspect.getfile(fn)).relative_to(PY_ROOT).as_posix()
    except Exception:  # noqa: BLE001
        return None


def closure(mod_rel, seen):
    """Transitive core.* import closure with line counts and markers."""
    if mod_rel in seen:
        return
    path = PY_ROOT / mod_rel
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8-sig")
    seen[mod_rel] = {
        "lines": text.count("\n") + 1,
        "markers": sorted({m for m in list(PLATFORM_MARKERS) + list(NETWORK_MARKERS)
                           if (m + " ") in text or ("import " + m) in text or ("from " + m) in text
                           or (m == "sys.platform" and "sys.platform" in text)
                           or (m == "playwright" and "playwright" in text)}),
        "uses_bs4": "from bs4" in text or "import bs4" in text,
    }
    tree = ast.parse(text)
    for node in ast.walk(tree):
        mods = []
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
            mods.append(node.module)
        elif isinstance(node, ast.Import):
            mods += [a.name for a in node.names if a.name.startswith("core.")]
        for m in mods:
            closure(m.replace(".", "/") + ".py", seen)


DART_ROOT = Path(r"C:\Projects\WebWeaveX")


def dart_counterpart_exists(mod_rel: str) -> bool:
    # core/a/b_engine.py -> lib/src/a/b_engine.dart (project convention), with
    # a fallback scan for the bare filename anywhere under lib/src.
    p = Path(mod_rel)
    cand = DART_ROOT / "lib" / "src" / Path(*p.parts[1:]).with_suffix(".dart")
    if cand.exists():
        return True
    name = p.with_suffix(".dart").name
    return name in _dart_files


_dart_files = {f.name for f in (DART_ROOT / "lib" / "src").rglob("*.dart")}


def main():
    report = {"generated_from": "python branch d4c5800 source (AST), zero-trust", "apis": []}
    totals = {"portable": 0, "platform_bound": 0, "total_unique_lines": 0}
    all_modules = {}
    for api in sorted(MISSING):
        fn = getattr(w, api, None)
        if fn is None:
            report["apis"].append({"api": api, "error": "not found in webweavex"})
            continue
        mod = module_of(fn)
        try:
            sig = api + str(inspect.signature(fn))
        except (TypeError, ValueError):
            sig = api + "(...)"
        seen = {}
        if mod:
            closure(mod, seen)
        markers = sorted({m for info in seen.values() for m in info["markers"]})
        uses_bs4 = any(info["uses_bs4"] for info in seen.values())
        platform = [PLATFORM_MARKERS[m] for m in markers if m in PLATFORM_MARKERS]
        network = [NETWORK_MARKERS[m] for m in markers if m in NETWORK_MARKERS]
        blocking = ("PLATFORM-BOUND: " + "; ".join(sorted(set(platform)))) if platform else \
                   ("PORTABLE (network-input variant: fetch via package:http like render_page)" if network else "PORTABLE (pure compute)")
        lines = sum(info["lines"] for info in seen.values())
        missing_mods = {m: i for m, i in seen.items() if not dart_counterpart_exists(m)}
        report["apis"].append({
            "api": api,
            "module": mod,
            "signature": sig,
            "dependencies_core_modules": len(seen),
            "dependency_modules_missing_in_dart": sorted(missing_mods.keys()),
            "modules_already_in_dart": len(seen) - len(missing_mods),
            "uses_bs4": uses_bs4,
            "estimated_port_lines_total_closure": lines,
            "estimated_port_lines_remaining": sum(i["lines"] for i in missing_mods.values()),
            "blocking_status": blocking,
        })
        if platform:
            totals["platform_bound"] += 1
        else:
            totals["portable"] += 1
        all_modules.update(seen)
    totals["total_unique_lines"] = sum(i["lines"] for i in all_modules.values())
    totals["unique_modules"] = len(all_modules)
    report["totals"] = totals
    json.dump(report, open("dart_extraction_gap_report.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(totals, indent=1))
    for a in report["apis"]:
        print(f"{a['api']:28s} {a.get('dependencies_core_modules', 0):3d} mods "
              f"({len(a.get('dependency_modules_missing_in_dart', [])):3d} missing, "
              f"{a.get('estimated_port_lines_remaining', 0):5d}L remain) "
              f"bs4={a.get('uses_bs4')} {a.get('blocking_status', '')[:45]}")


if __name__ == "__main__":
    main()
