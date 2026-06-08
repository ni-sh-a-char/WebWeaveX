#!/usr/bin/env python3
"""
Phase 1 + 2: Live forensic true-equality audit and generated-code audit.
Never issues certification — reports measured gates only.
"""
from __future__ import annotations

import json
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs" / "archive"
SPECS = ROOT / "docs" / "specs"
PROTECTED = ROOT / "tools/convergence/protected_js.txt"
VECTORS = ROOT / "validation/vectors"


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def count_glob(base: Path, pattern: str) -> int:
    return sum(1 for _ in base.rglob(pattern))


def npm_cmd(script: str) -> list[str] | str:
    if platform.system() == "Windows":
        return f"npm run {script}"
    return ["npm", "run", script]


def run_npm(script: str, timeout: int = 600) -> tuple[int, str]:
    proc = subprocess.run(
        npm_cmd(script),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        shell=platform.system() == "Windows",
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def differential_status() -> dict:
    code, out = run_npm("validate:differential", timeout=900)
    families: dict[str, str] = {}
    for line in out.splitlines():
        if line.startswith("## ") and "[" in line:
            m = re.match(r"## (.+?) \[(PASS|FAIL)\]", line)
            if m:
                families[m.group(1)] = m.group(2)
    return {
        "exit_code": code,
        "passed": code == 0,
        "families": families,
        "families_passed": sum(1 for v in families.values() if v == "PASS"),
        "families_total": len(families),
    }


def coverage_status() -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "tools/convergence/coverage_probe.py")],
        cwd=ROOT,
        capture_output=True,
        timeout=900,
    )
    probe = SPECS / "coverage_probe.json"
    if probe.exists():
        return json.loads(probe.read_text(encoding="utf-8"))
    return {}


def readme_sections() -> int:
    readme = ROOT / "README.md"
    if not readme.exists():
        return 0
    return sum(1 for ln in readme.read_text(encoding="utf-8").splitlines() if ln.startswith("## "))


def ts_nocheck_audit() -> dict:
    protected: set[str] = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}
    generated: list[Path] = []
    nocheck_generated = 0
    for p in (ROOT / "src").rglob("*.ts"):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel in protected:
            continue
        generated.append(p)
        if "@ts-nocheck" in p.read_text(encoding="utf-8", errors="replace"):
            nocheck_generated += 1
    return {
        "generated_total": len(generated),
        "nocheck_generated": nocheck_generated,
        "protected_total": len(protected),
    }


def export_symbols(ts_path: Path) -> list[str]:
    text = ts_path.read_text(encoding="utf-8", errors="replace")
    symbols: list[str] = []
    for m in re.finditer(r"^export (?:async )?function (\w+)", text, re.M):
        symbols.append(f"function:{m.group(1)}")
    for m in re.finditer(r"^export class (\w+)", text, re.M):
        symbols.append(f"class:{m.group(1)}")
    for m in re.finditer(r"^export const (\w+)", text, re.M):
        symbols.append(f"const:{m.group(1)}")
    return symbols


def write_generated_code_audit(ts: str, nocheck: dict) -> None:
    protected: set[str] = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}
    sys.path.insert(0, str(ROOT / "tools/py2ts"))
    from py2ts import py_path_to_ts  # noqa: E402

    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    rows: list[dict] = []
    sample = py_mods[:500]
    for py in sample:
        ts_rel = "src/" + py_path_to_ts(py)
        ts_path = ROOT / ts_rel
        row = {
            "python_source": py,
            "ts_target": ts_rel,
            "exists": ts_path.exists(),
            "protected": ts_rel in protected,
            "ts_nocheck": False,
            "exported_symbols": [],
            "behavioral_probe": "NOT RUN",
        }
        if ts_path.exists():
            text = ts_path.read_text(encoding="utf-8", errors="replace")
            row["ts_nocheck"] = "@ts-nocheck" in text
            row["exported_symbols"] = export_symbols(ts_path)[:20]
        rows.append(row)

    body = "\n".join(
        [
            "# FINAL GENERATED CODE AUDIT",
            "",
            f"**Measured:** {ts}",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Python `core/*.py` modules | {len(py_mods)} |",
            f"| Generated TS (non-protected) | {nocheck['generated_total']} |",
            f"| `@ts-nocheck` in generated | {nocheck['nocheck_generated']} |",
            f"| Protected operational modules | {nocheck['protected_total']} |",
            f"| Sample audited (first 500 py paths) | {len(sample)} |",
            "",
            "## Verdict",
            "",
            "**Generated module behavioral validation: NOT COMPLETE**",
            "",
            "Topology mirrors exist for most modules; per-module execution probes are not automated at scale.",
            "Protected modules are hand-authored overrides and require differential vectors + targeted tests.",
            "",
            "## Sample module registry",
            "",
            "| Python | TypeScript | Exists | Protected | @ts-nocheck | Exports (sample) |",
            "|--------|------------|--------|-----------|-------------|------------------|",
        ]
    )
    for r in rows[:100]:
        exports = ", ".join(r["exported_symbols"][:5]) or "—"
        body += (
            f"| `{r['python_source']}` | `{r['ts_target']}` | "
            f"{'yes' if r['exists'] else 'no'} | {'yes' if r['protected'] else 'no'} | "
            f"{'yes' if r['ts_nocheck'] else 'no'} | {exports} |"
        )
    body += "\n\n```json\n" + json.dumps({"sample": rows[:50], "nocheck": nocheck}, indent=2) + "\n```\n"
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_GENERATED_CODE_AUDIT.md").write_text(body, encoding="utf-8")
    print("  FINAL_GENERATED_CODE_AUDIT.md")


def write_true_equality_audit(
    ts: str,
    py_mod: int,
    js_mod: int,
    diff: dict,
    cov: dict,
    nocheck: dict,
) -> None:
    tests_py = len(git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "tests/"))
    tests_js = count_glob(ROOT / "tests", "*.ts")
    sections = readme_sections()
    vector_families = sorted(
        p.name for p in VECTORS.iterdir() if p.is_dir() and (p / "canonical.json").exists()
    )

    def gate(label: str, ok: bool, detail: str) -> str:
        return f"| {label} | {'PASS' if ok else '**FAIL**'} | {detail} |"

    cov_ok = bool(cov.get("threshold_met"))
    diff_ok = diff.get("passed", False)
    readme_ok = sections >= 30
    tests_ok = tests_js >= max(200, int(tests_py * 0.35))
    nocheck_ok = nocheck["nocheck_generated"] == 0
    topology_ok = js_mod >= py_mod * 0.99

    body = "\n".join(
        [
            "# FINAL TRUE EQUALITY AUDIT",
            "",
            f"**Measured:** {ts}",
            "",
            "**STATUS: TRUE EQUALITY NOT ACHIEVED**",
            "",
            "This report is derived from live git data, vector families, and executable validators.",
            "Certification is explicitly withheld until all behavioral gates pass.",
            "",
            "## Gate matrix",
            "",
            "| Domain | Status | Evidence |",
            "|--------|--------|----------|",
            gate("Topology", topology_ok, f"JS modules {js_mod} vs Python {py_mod}"),
            gate("Runtime (differential)", diff_ok, f"{diff.get('families_passed', 0)}/{diff.get('families_total', 0)} families"),
            gate("Memory (vectors)", "Memory equivalence" in diff.get("families", {}) and diff["families"].get("Memory equivalence") == "PASS", "memory_vectors + validateMemoryEquivalence"),
            gate("Reconstruction (vectors)", "Reconstruction equivalence" in diff.get("families", {}) and diff["families"].get("Reconstruction equivalence") == "PASS", "reconstruction_vectors"),
            gate("Semantic (vectors)", diff["families"].get("Semantic equivalence") == "PASS" if diff.get("families") else False, "semantic_vectors"),
            gate("Ontology (vectors)", diff["families"].get("Ontology equivalence") == "PASS" if diff.get("families") else False, "ontology_vectors"),
            gate("Workflow (vectors)", diff["families"].get("Workflow equivalence") == "PASS" if diff.get("families") else False, "workflow_vectors"),
            gate("Distributed (vectors)", diff["families"].get("Distributed equivalence") == "PASS" if diff.get("families") else False, "distributed_vectors"),
            gate("Replay (vectors)", diff["families"].get("Replay equivalence") == "PASS" if diff.get("families") else False, "replay_vectors"),
            gate("VM (vectors)", diff["families"].get("VM equivalence") == "PASS" if diff.get("families") else False, "vm_vectors"),
            gate("Graph (vectors)", diff["families"].get("Graph equivalence") == "PASS" if diff.get("families") else False, "graph_vectors"),
            gate("Generated ports (execution)", False, f"{nocheck['nocheck_generated']} @ts-nocheck generated files"),
            gate("Coverage (98/98/98/95)", cov_ok, json.dumps(cov)),
            gate("Documentation (README ≥30)", readme_ok, f"{sections} sections"),
            gate("Test depth", tests_ok, f"JS {tests_js} vs Python {tests_py} files"),
            gate("@ts-nocheck eliminated", nocheck_ok, f"{nocheck['nocheck_generated']} remaining"),
            "",
            "## Topology",
            "",
            f"- Python `core/*.py`: **{py_mod}**",
            f"- JavaScript `src/*.ts`: **{js_mod}**",
            f"- Vector families present: **{len(vector_families)}** ({', '.join(vector_families)})",
            "",
            "## Differential families (live)",
            "",
        ]
    )
    for name, status in sorted(diff.get("families", {}).items()):
        body += f"- {name}: **{status}**\n"
    if not diff.get("families"):
        body += "- _Differential suite did not run or produced no family output._\n"

    body += "\n## Required commands (all must pass for certification)\n\n"
    body += "```bash\nnpm install\nnpm run build\nnpm run test\nnpm run coverage\nnpm run validate:parity\nnpm run validate:differential\nnpm run validate:ecosystem\nnpm run convergence:vectors\nnpm run convergence:verify-ports\npython -B tools/convergence/forensic_equality_audit.py\n```\n"

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_TRUE_EQUALITY_AUDIT.md").write_text(body, encoding="utf-8")
    print("  FINAL_TRUE_EQUALITY_AUDIT.md")


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    py_mod = sum(1 for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py"))
    js_mod = count_glob(ROOT / "src", "*.ts")
    nocheck = ts_nocheck_audit()
    print("Running differential validators…")
    diff = differential_status()
    print("Running coverage probe…")
    cov = coverage_status()
    write_true_equality_audit(ts, py_mod, js_mod, diff, cov, nocheck)
    write_generated_code_audit(ts, nocheck)
    certified = (
        diff.get("passed")
        and cov.get("threshold_met")
        and nocheck["nocheck_generated"] == 0
        and readme_sections() >= 30
    )
    print(f"\nCertification eligible: {certified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
