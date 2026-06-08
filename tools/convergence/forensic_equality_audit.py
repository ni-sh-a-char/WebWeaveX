#!/usr/bin/env python3
"""
Phase 1 + 11: Live forensic equality audit (JavaScript vs Python).
Uses git + worktree only. No cached estimates.
"""
from __future__ import annotations

import json
import platform
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs" / "archive"
SPECS = ROOT / "docs" / "specs"
def _npm_cmd(script: str) -> list[str] | str:
    if platform.system() == "Windows":
        return f"npm run {script}"
    return ["npm", "run", script]


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def snake_to_camel(s: str) -> str:
    parts = s.replace(".py", "").split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def py_top_level_packages() -> set[str]:
    dirs = git_lines("ls-tree", "--name-only", "-d", "origin/python", "core/")
    pkgs = set()
    for d in dirs:
        parts = d.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "core" and parts[1]:
            pkgs.add(parts[1])
    # root-level modules core/foo.py
    for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/"):
        if not p.endswith(".py"):
            continue
        parts = p.split("/")
        if len(parts) == 2 and parts[1] != "__init__.py":
            pkgs.add("(root)")
    return pkgs


def js_top_level_packages() -> set[str]:
    src = ROOT / "src"
    if not src.exists():
        return set()
    pkgs = {d.name for d in src.iterdir() if d.is_dir()}
    if any(src.glob("*.ts")):
        pkgs.add("(root)")
    # normalize worldModel -> world_model for compare
    normalized = set()
    for p in pkgs:
        if p == "worldModel":
            normalized.add("world_model")
        else:
            normalized.add(p)
    return normalized


def count_glob(root: Path, pattern: str) -> int:
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob(pattern) if _.is_file())


def py_validators() -> list[str]:
    return sorted(
        p
        for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "validation/")
        if p.endswith(".py") and "validate" in p.lower()
    )


def js_validators() -> list[str]:
    val = ROOT / "validation"
    if not val.exists():
        return []
    return sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in val.rglob("validate*.ts"))


def py_validator_to_camel(py_path: str) -> str:
    stem = Path(py_path).stem
    parts = stem.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def py_validator_mirrored(py_path: str, js_paths: list[str]) -> bool:
    """Map Python validation/*.py to JS validate*.ts mirrors (folder or camel stem)."""
    camel = py_validator_to_camel(py_path)
    folder = Path(py_path).parent.name
    aliases = {
        "validation/kaalka_cross_language/validate_cross_language.py": [
            "validateCrossLanguage",
            "validateParity",
            "kaalka_cross_language",
        ],
        "validation/validate_cross_language_parity.py": ["validateParity", "validate_cross_language"],
    }
    checks = {camel.lower(), Path(py_path).stem.lower()}
    if py_path in aliases:
        checks.update(a.lower() for a in aliases[py_path])
    if folder not in ("validation", ""):
        checks.add(folder.lower())
    for j in js_paths:
        jl = j.lower().replace("\\", "/")
        if any(c in jl for c in checks if len(c) > 4):
            return True
        if folder not in ("validation", "") and folder in jl and "validate" in jl:
            return True
    return False


def governance_set(ref: str) -> set[str]:
    candidates = [
        "CODEOWNERS",
        "CONTRIBUTING.md",
        "GOVERNANCE.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "MAINTAINERS.md",
        "ROADMAP.md",
        "SUPPORT.md",
        "RELEASE.md",
        "LICENSE",
        ".github/FUNDING.yml",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ]
    present = set()
    for c in candidates:
        if git_lines("ls-tree", ref, "--", c):
            present.add(c)
    for p in git_lines("ls-tree", "-r", "--name-only", ref, "--", ".github/ISSUE_TEMPLATE/"):
        present.add(p)
    for p in git_lines("ls-tree", "-r", "--name-only", ref, "--", ".github/workflows/"):
        if p.endswith((".yml", ".yaml")):
            present.add(p)
    return present


def write(name: str, body: str) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / name).write_text(body, encoding="utf-8")
    print(f"  {name}")


def readme_section_count() -> int:
    readme = ROOT / "README.md"
    if not readme.exists():
        return 0
    return sum(1 for ln in readme.read_text(encoding="utf-8").splitlines() if ln.startswith("## "))


def generated_port_execution_proven() -> bool:
    """True only when port verification explicitly marks execution equivalence proven."""
    report = ARCHIVE / "FINAL_GENERATED_PORT_VERIFICATION.md"
    if not report.exists():
        return False
    text = report.read_text(encoding="utf-8")
    if "**Generated port behavioral equivalence: PROVEN**" in text:
        return True
    m = re.search(r'"execution_equivalence_proven"\s*:\s*true', text)
    return bool(m)


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    py_mod = len(git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/"))
    py_mod = sum(1 for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py"))
    js_mod = count_glob(ROOT / "src", "*.ts")
    js_mod_git = sum(1 for p in git_lines("ls-tree", "-r", "--name-only", "HEAD", "--", "src/") if p.endswith(".ts"))

    py_pkgs = py_top_level_packages()
    js_pkgs = js_top_level_packages()
    missing_pkgs = sorted(py_pkgs - js_pkgs)
    extra_pkgs = sorted(js_pkgs - py_pkgs)

    py_val = py_validators()
    js_val = js_validators()
    gov_py = governance_set("origin/python")
    gov_js = governance_set("HEAD")
    gov_wt = governance_set("HEAD")  # worktree same ref; check files exist
    for g in list(gov_py | {"GOVERNANCE.md", "MAINTAINERS.md", "SUPPORT.md", "RELEASE.md", "CODEOWNERS"}):
        if (ROOT / g).exists() or (ROOT / Path(g)).exists():
            gov_wt.add(g)

    missing_gov = sorted(gov_py - gov_wt)
    missing_val = [v for v in py_val if not py_validator_mirrored(v, js_val)]

    coverage_branches: float | None = None
    cov_probe = subprocess.run(
        [sys.executable, str(ROOT / "tools/convergence/coverage_probe.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
    )
    coverage_branches = None
    coverage_metrics: dict = {}
    probe_path = SPECS / "coverage_probe.json"
    if probe_path.exists():
        coverage_metrics = json.loads(probe_path.read_text(encoding="utf-8"))
        coverage_branches = coverage_metrics.get("branches_pct")
    if coverage_metrics.get("branches_pct") is None and cov_probe.returncode != 0:
        retry = subprocess.run(
            [sys.executable, str(ROOT / "tools/convergence/coverage_probe.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        if probe_path.exists():
            coverage_metrics = json.loads(probe_path.read_text(encoding="utf-8"))
            coverage_branches = coverage_metrics.get("branches_pct")

    parity_ok = False
    parity_run = subprocess.run(
        _npm_cmd("validate:parity"),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        shell=platform.system() == "Windows",
    )
    parity_ok = parity_run.returncode == 0

    diff_ok = False
    diff_families_passed = 0
    diff_families_total = 0
    diff_run = subprocess.run(
        _npm_cmd("validate:differential"),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
        shell=platform.system() == "Windows",
    )
    diff_out = (diff_run.stdout or "") + (diff_run.stderr or "")
    for line in diff_out.splitlines():
        if "[PASS]" in line:
            diff_families_passed += 1
            diff_families_total += 1
        elif "[FAIL]" in line:
            diff_families_total += 1
    diff_ok = diff_run.returncode == 0

    tests_py = len(git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "tests/"))
    tests_js = count_glob(ROOT / "tests", "*.ts")

    workflows_py = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", ".github/workflows/") if p.endswith(".yml")]
    workflows_js = [p for p in git_lines("ls-tree", "-r", "--name-only", "HEAD", "--", ".github/workflows/") if p.endswith(".yml")]
    if (ROOT / ".github/workflows").exists():
        workflows_js = [str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / ".github/workflows").glob("*.yml")]

    subprocess.run(
        [sys.executable, str(ROOT / "tools/convergence/verify_generated_ports.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )

    coverage_full_ok = bool(coverage_metrics.get("threshold_met"))
    readme_sections = readme_section_count()
    readme_ok = readme_sections >= 30
    generated_ports_ok = generated_port_execution_proven()
    tests_depth_ratio = (tests_js / tests_py) if tests_py else 0.0
    tests_depth_ok = tests_js >= max(200, int(tests_py * 0.35))
    ecosystem_ok = False
    eco_run = subprocess.run(
        _npm_cmd("validate:ecosystem"),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
        shell=platform.system() == "Windows",
    )
    ecosystem_ok = eco_run.returncode == 0

    behavioral_equivalence_proven = (
        diff_ok
        and parity_ok
        and generated_ports_ok
        and ecosystem_ok
    )

    certified = (
        js_mod >= py_mod * 0.99
        and not missing_pkgs
        and len(missing_gov) == 0
        and len(missing_val) == 0
        and coverage_full_ok
        and parity_ok
        and diff_ok
        and behavioral_equivalence_proven
        and readme_ok
        and tests_depth_ok
        and generated_ports_ok
        and ecosystem_ok
    )

    inventory = {
        "measured_at": ts,
        "python": {
            "ref": "origin/python",
            "core_modules": py_mod,
            "top_level_packages": len(py_pkgs),
            "validators": py_val,
            "validator_count": len(py_val),
            "tests": tests_py,
            "workflows": workflows_py,
            "governance": sorted(gov_py),
        },
        "javascript": {
            "ref": "javascript worktree",
            "src_modules": js_mod,
            "src_modules_git": js_mod_git,
            "top_level_packages": len(js_pkgs),
            "validators": js_val,
            "validator_count": len(js_val),
            "tests": tests_js,
            "workflows": workflows_js,
            "governance": sorted(gov_wt),
            "module_depth_pct": round(js_mod / py_mod * 100, 2) if py_mod else 0,
        },
        "gaps": {
            "packages_missing_in_javascript": missing_pkgs,
            "packages_extra_in_javascript": extra_pkgs,
            "governance_missing": missing_gov,
            "validators_not_mirrored": missing_val,
        },
        "coverage": {
            **coverage_metrics,
            "branches_pct": coverage_branches,
            "threshold_met": coverage_full_ok,
        },
        "parity_validation_passed": parity_ok,
        "ecosystem_validation_passed": ecosystem_ok,
        "differential_equivalence": {
            "passed": diff_ok,
            "families_passed": diff_families_passed,
            "families_total": diff_families_total,
        },
        "docs": {
            "readme_sections": readme_sections,
            "readme_target_met": readme_ok,
        },
        "tests": {
            "javascript_files": tests_js,
            "python_files": tests_py,
            "depth_ratio": round(tests_depth_ratio, 4),
            "depth_target_met": tests_depth_ok,
        },
        "generated_port_execution_proven": generated_ports_ok,
        "behavioral_equivalence_proven": behavioral_equivalence_proven,
        "true_equality_certified": certified,
    }

    SPECS.mkdir(parents=True, exist_ok=True)
    (SPECS / "forensic_inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")

    print("Forensic equality audit:")
    for report in [
        ("FINAL_FORENSIC_EQUALITY_AUDIT.md", _forensic_audit(ts, inventory)),
        ("FINAL_FILE_DEPTH_MATRIX.md", _file_matrix(ts, py_mod, js_mod)),
        ("FINAL_RUNTIME_MATRIX.md", _subsystem_matrix(ts, "runtime", inventory)),
        ("FINAL_VM_MATRIX.md", _subsystem_matrix(ts, "vm", inventory)),
        ("FINAL_GRAPH_MATRIX.md", _subsystem_matrix(ts, "graph", inventory)),
        ("FINAL_SEMANTIC_MATRIX.md", _subsystem_matrix(ts, "semantic", inventory)),
        ("FINAL_VALIDATION_MATRIX.md", _validation_matrix(ts, inventory)),
        ("FINAL_GOVERNANCE_MATRIX.md", _governance_matrix(ts, inventory)),
        ("FINAL_OSS_MATRIX.md", _oss_matrix(ts, inventory)),
        ("FINAL_REPLAY_MATRIX.md", _subsystem_matrix(ts, "replay", inventory)),
        ("FINAL_CONTRACT_MATRIX.md", _contract_matrix(ts)),
        ("FINAL_RELEASE_MATRIX.md", _release_matrix(ts, inventory)),
        ("FINAL_CONVERGENCE_REPORT.md", _convergence_report(ts, inventory)),
        ("FINAL_PARITY_PROOF.md", _parity_proof(ts, inventory)),
        ("FINAL_DOCS_EQUALITY_REPORT.md", _docs_equality_report(ts, inventory)),
    ]:
        write(report[0], report[1])

    if certified:
        write("FINAL_TRUE_EQUALITY_CERTIFICATION.md", _certification(ts, inventory, issued=True))
    else:
        write("FINAL_TRUE_EQUALITY_CERTIFICATION.md", _certification(ts, inventory, issued=False))


def _forensic_audit(ts: str, inv: dict) -> str:
    py = inv["python"]
    js = inv["javascript"]
    gaps = inv["gaps"]
    return "\n".join(
        [
            "# FINAL FORENSIC EQUALITY AUDIT",
            "",
            f"**Measured (UTC):** {ts}",
            "",
            "## Module inventory",
            "",
            f"| Metric | Python | JavaScript |",
            f"|--------|--------|------------|",
            f"| Core modules | {py['core_modules']} | {js['src_modules']} |",
            f"| Depth % | 100% | {js['module_depth_pct']}% |",
            f"| Top-level packages | {py['top_level_packages']} | {js['top_level_packages']} |",
            f"| Tests | {py['tests']} | {js['tests']} |",
            f"| Validators | {py['validator_count']} | {js['validator_count']} |",
            "",
            "## Missing packages (directory topology)",
            "",
            *(
                [f"- `{p}`" for p in gaps["packages_missing_in_javascript"]]
                if gaps["packages_missing_in_javascript"]
                else ["- none"]
            ),
            "",
            "## Governance gaps",
            "",
            *(
                [f"- `{g}`" for g in gaps["governance_missing"]]
                if gaps["governance_missing"]
                else ["- none"]
            ),
            "",
            "## Verdict",
            "",
            "**TRUE EQUALITY: NOT ACHIEVED**" if not inv["true_equality_certified"] else "**TRUE EQUALITY: ACHIEVED**",
            "",
        ]
    )


def _file_matrix(ts: str, py_mod: int, js_mod: int) -> str:
    return "\n".join(
        [
            "# FINAL FILE DEPTH MATRIX",
            "",
            f"**Measured:** {ts}",
            "",
            f"| Branch | Modules |",
            f"|--------|---------|",
            f"| Python | {py_mod} |",
            f"| JavaScript | {js_mod} |",
            f"| Delta | {js_mod - py_mod:+d} |",
            "",
            "**Note:** File depth exceeds Python; behavioral equivalence is separate (see FINAL_PARITY_PROOF.md).",
            "",
        ]
    )


def _subsystem_matrix(ts: str, name: str, inv: dict) -> str:
    py_paths = git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/")
    py_count = sum(1 for p in py_paths if name in p and p.endswith(".py"))
    js_count = sum(1 for _ in (ROOT / "src").rglob("*.ts") if name.replace("_", "") in str(_.as_posix()).lower())
    return "\n".join(
        [
            f"# FINAL {name.upper()} MATRIX",
            "",
            f"**Measured:** {ts}",
            "",
            f"| | Python modules | JS modules (path match) |",
            f"|--|----------------|-------------------------|",
            f"| {name} | {py_count} | {js_count} |",
            "",
            "**TRUE subsystem equality: NOT VERIFIED** without differential vector pass.",
            "",
        ]
    )


def _validation_matrix(ts: str, inv: dict) -> str:
    lines = [
        "# FINAL VALIDATION MATRIX",
        "",
        f"**Measured:** {ts}",
        "",
        "## Python validators",
        "",
    ]
    for v in inv["python"]["validators"]:
        lines.append(f"- `{v}`")
    lines.extend(["", "## JavaScript validators", ""])
    for v in inv["javascript"]["validators"]:
        lines.append(f"- `{v}`")
    lines.extend(
        [
            "",
            "## Coverage thresholds (required)",
            "",
            "- Lines ≥ 97%",
            "- Functions ≥ 98%",
            "- Statements ≥ 97%",
            "- Branches ≥ 90%",
            "",
        ]
    )
    return "\n".join(lines)


def _governance_matrix(ts: str, inv: dict) -> str:
    return "\n".join(
        [
            "# FINAL GOVERNANCE MATRIX",
            "",
            f"**Measured:** {ts}",
            "",
            "| Asset | Python | JavaScript (worktree) |",
            "|-------|--------|----------------------|",
            *[
                f"| `{g}` | {'yes' if g in inv['python']['governance'] else 'no'} | {'yes' if g in inv['javascript']['governance'] else 'no'} |"
                for g in sorted(set(inv["python"]["governance"]) | set(inv["javascript"]["governance"]) | {"GOVERNANCE.md", "MAINTAINERS.md", "SUPPORT.md", "RELEASE.md", "CODEOWNERS"})
            ],
            "",
        ]
    )


def _oss_matrix(ts: str, inv: dict) -> str:
    return "\n".join(
        [
            "# FINAL OSS MATRIX",
            "",
            f"**Measured:** {ts}",
            "",
            f"| Dimension | Python | JavaScript |",
            f"|-----------|--------|------------|",
            f"| Workflows | {len(inv['python']['workflows'])} | {len(inv['javascript']['workflows'])} |",
            f"| Tests | {inv['python']['tests']} | {inv['javascript']['tests']} |",
            "",
        ]
    )


def _contract_matrix(ts: str) -> str:
    specs = list(SPECS.glob("canonical_*.json")) if SPECS.exists() else []
    return "\n".join(
        [
            "# FINAL CONTRACT MATRIX",
            "",
            f"**Measured:** {ts}",
            "",
            "## Canonical specs",
            "",
            *(
                [f"- `{p.name}`" for p in sorted(specs)]
                if specs
                else ["- none (run tools/specgen/generate_all_specs.py)"]
            ),
            "",
        ]
    )


def _release_matrix(ts: str, inv: dict) -> str:
    return "\n".join(
        [
            "# FINAL RELEASE MATRIX",
            "",
            f"**Measured:** {ts}",
            "",
            "- npm: `package.json`, `prepublishOnly`, `tsup` dual ESM/CJS",
            "- Python: `pyproject.toml`, `MANIFEST.in`",
            "",
            "**Release parity: NOT ACHIEVED** until publish workflows and RELEASE.md mirror.",
            "",
        ]
    )


def _convergence_report(ts: str, inv: dict) -> str:
    return "\n".join(
        [
            "# FINAL CONVERGENCE REPORT",
            "",
            f"**Measured:** {ts}",
            "",
            "JavaScript convergence phase: file topology largely mirrored; behavioral, validator, governance, and coverage gates remain open.",
            "",
            f"See `docs/specs/forensic_inventory.json` for machine-readable state.",
            "",
        ]
    )


def _docs_equality_report(ts: str, inv: dict) -> str:
    readme = ROOT / "README.md"
    sections = 0
    if readme.exists():
        sections = sum(1 for ln in readme.read_text(encoding="utf-8").splitlines() if ln.startswith("## "))
    py_readme_sections = 0
    py_readme = subprocess.run(
        ["git", "show", "origin/python:README.md"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if py_readme.returncode == 0:
        py_readme_sections = sum(1 for ln in py_readme.stdout.splitlines() if ln.startswith("## "))
    return "\n".join(
        [
            "# FINAL DOCS EQUALITY REPORT",
            "",
            f"**Measured:** {ts}",
            "",
            f"| Metric | Python | JavaScript |",
            f"|--------|--------|------------|",
            f"| README `##` sections | {py_readme_sections} | {sections} |",
            f"| Target (30+ sections) | — | {'met' if sections >= 30 else 'NOT met'} |",
            "",
            "**Docs parity: NOT ACHIEVED**"
            if sections < 30 or sections < py_readme_sections
            else "**Docs parity: partial**",
            "",
        ]
    )


def _parity_proof(ts: str, inv: dict) -> str:
    return "\n".join(
        [
            "# FINAL PARITY PROOF",
            "",
            f"**Measured:** {ts}",
            "",
            f"- Module files: JS {inv['javascript']['src_modules']} vs Python {inv['python']['core_modules']}",
            f"- Differential replay/graph/VM vectors: run `npm run validate:parity`",
            "",
            "**Cryptographic parity proof across full core: NOT COMPLETE.**",
            "",
        ]
    )


def _certification(ts: str, inv: dict, *, issued: bool) -> str:
    if issued:
        return f"# FINAL TRUE EQUALITY CERTIFICATION\n\n**Issued:** {ts}\n\nAll gates passed.\n"
    gaps = inv["gaps"]
    return "\n".join(
        [
            "# FINAL TRUE EQUALITY CERTIFICATION",
            "",
            "**STATUS: NOT ISSUED**",
            "",
            f"**Measured:** {ts}",
            "",
            "## Blocking items",
            "",
            *(f"- Missing package: `{p}`" for p in gaps["packages_missing_in_javascript"]),
            *(f"- Missing governance: `{g}`" for g in gaps["governance_missing"]),
            *(
                [f"- Validator parity: {len(gaps['validators_not_mirrored'])} Python scripts without JS mirror"]
                if gaps["validators_not_mirrored"]
                else []
            ),
            *(
                [
                    f"- Coverage thresholds (98/98/98/95): "
                    f"lines={inv.get('coverage', {}).get('lines_pct')}% "
                    f"funcs={inv.get('coverage', {}).get('functions_pct')}% "
                    f"stmts={inv.get('coverage', {}).get('statements_pct')}% "
                    f"branches={inv.get('coverage', {}).get('branches_pct')}% "
                    f"({'PASS' if inv.get('coverage', {}).get('threshold_met') else 'FAIL'})"
                ]
            ),
            *(
                [
                    f"- README sections (≥30): {inv.get('docs', {}).get('readme_sections', 0)} "
                    f"({'PASS' if inv.get('docs', {}).get('readme_target_met') else 'FAIL'})"
                ]
            ),
            *(
                [
                    f"- Test depth: JS {inv.get('tests', {}).get('javascript_files', 0)} vs "
                    f"Python {inv.get('tests', {}).get('python_files', 0)} "
                    f"({'PASS' if inv.get('tests', {}).get('depth_target_met') else 'FAIL'})"
                ]
            ),
            *(
                [
                    "- Ecosystem validation: "
                    + ("PASS" if inv.get("ecosystem_validation_passed") else "FAIL — run `npm run validate:ecosystem`")
                ]
            ),
            *(
                [
                    "- Differential / parity validation: "
                    + ("PASS" if inv.get("parity_validation_passed") else "FAIL — run `npm run validate:parity`")
                ]
            ),
            *(
                [
                    "- Differential equivalence (Python vectors → JS): "
                    + (
                        "PASS ("
                        + str(inv.get("differential_equivalence", {}).get("families_passed", 0))
                        + "/"
                        + str(inv.get("differential_equivalence", {}).get("families_total", 0))
                        + " families)"
                        if inv.get("differential_equivalence", {}).get("passed")
                        else "FAIL ("
                        + str(inv.get("differential_equivalence", {}).get("families_passed", 0))
                        + "/"
                        + str(inv.get("differential_equivalence", {}).get("families_total", 0))
                        + " families pass)"
                    )
                ]
            ),
            *(
                [
                    "- Generated-port execution equivalence: "
                    + ("PROVEN" if inv.get("generated_port_execution_proven") else "NOT PROVEN")
                ]
            ),
            "",
            "TRUE EQUALITY NOT ACHIEVED. Convergence continues.",
            "",
        ]
    )


if __name__ == "__main__":
    main()
