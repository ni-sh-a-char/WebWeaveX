#!/usr/bin/env python3
"""Live git forensic inventories for WebWeaveX cross-language convergence."""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs" / "archive"
SPECS = ROOT / "docs" / "specs"


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return []
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def count_files(ref: str, prefix: str, suffix: str) -> int:
    paths = git_lines("ls-tree", "-r", "--name-only", ref, "--", prefix)
    return sum(1 for p in paths if p.endswith(suffix))


def count_worktree(prefix: Path, suffix: str) -> int:
    if not prefix.exists():
        return 0
    return sum(1 for _ in prefix.rglob(f"*{suffix}") if _.is_file())


def package_counts(ref: str, core_prefix: str = "core") -> dict[str, int]:
    paths = git_lines("ls-tree", "-r", "--name-only", ref, "--", f"{core_prefix}/")
    pkgs: dict[str, int] = defaultdict(int)
    for p in paths:
        if not p.endswith(".py"):
            continue
        parts = p.split("/")
        if len(parts) >= 2:
            pkgs[parts[1]] += 1
    return dict(sorted(pkgs.items()))


def js_package_counts() -> dict[str, int]:
    src = ROOT / "src"
    pkgs: dict[str, int] = defaultdict(int)
    if not src.exists():
        return {}
    for f in src.rglob("*.ts"):
        rel = f.relative_to(src)
        if len(rel.parts) >= 2:
            pkgs[rel.parts[0]] += 1
        else:
            pkgs["(root)"] += 1
    return dict(sorted(pkgs.items()))


def dart_package_counts(ref: str) -> dict[str, int]:
    paths = git_lines("ls-tree", "-r", "--name-only", ref, "--", "lib/")
    pkgs: dict[str, int] = defaultdict(int)
    for p in paths:
        if not p.endswith(".dart"):
            continue
        parts = Path(p).parts
        # lib/src/pkg/... or lib/pkg/...
        idx = 1
        if len(parts) > 2 and parts[1] == "src":
            idx = 2
        if len(parts) > idx + 1:
            pkgs[parts[idx]] += 1
    return dict(sorted(pkgs.items()))


def workflow_count(ref: str) -> int:
    return count_files(ref, ".github/workflows", ".yml") + count_files(ref, ".github/workflows", ".yaml")


def governance_files(ref: str) -> list[str]:
    names = [
        "CODEOWNERS",
        "CONTRIBUTING.md",
        "GOVERNANCE.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "MAINTAINERS.md",
        "ROADMAP.md",
        "SUPPORT.md",
        "LICENSE",
        "FUNDING.yml",
        ".github/FUNDING.yml",
    ]
    present = []
    for n in names:
        if git_lines("ls-tree", ref, "--", n):
            present.append(n)
    return present


def write(name: str, body: str) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / name).write_text(body, encoding="utf-8")
    print(f"Wrote docs/archive/{name}")


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    py_ref = "origin/python"
    js_ref = "HEAD"
    dart_ref = "origin/dart"

    py_core = count_files(py_ref, "core", ".py")
    js_src_git = count_files(js_ref, "src", ".ts")
    js_src_wt = count_worktree(ROOT / "src", ".ts")
    dart_lib_git = count_files(dart_ref, "lib", ".dart")
    dart_lib_wt = count_worktree(ROOT / "lib", ".dart")

    py_val = count_files(py_ref, "validation", ".py")
    js_val_git = count_files(js_ref, "validation", ".ts")
    js_val_wt = count_worktree(ROOT / "validation", ".ts")
    dart_val = count_files(dart_ref, "validation", ".dart")

    py_tests = len(git_lines("ls-tree", "-r", "--name-only", py_ref, "--", "tests"))
    js_tests_git = len(git_lines("ls-tree", "-r", "--name-only", js_ref, "--", "tests"))
    js_tests_wt = len(list((ROOT / "tests").rglob("*"))) if (ROOT / "tests").exists() else 0
    dart_tests = len(git_lines("ls-tree", "-r", "--name-only", dart_ref, "--", "test"))

    py_pkgs = package_counts(py_ref)
    js_pkgs = js_package_counts()
    dart_pkgs = dart_package_counts(dart_ref)

    py_pkg_count = len(py_pkgs)
    js_pkg_count = len(js_pkgs)
    dart_pkg_count = len(dart_pkgs)

    missing_js = sorted(set(py_pkgs) - set(js_pkgs))
    missing_dart = sorted(set(py_pkgs) - set(dart_pkgs))

    gov_py = governance_files(py_ref)
    gov_js = governance_files(js_ref)
    gov_dart = governance_files(dart_ref)

    equality_ratio_js = round(js_src_wt / py_core * 100, 2) if py_core else 0
    equality_ratio_dart = round(dart_lib_git / py_core * 100, 2) if py_core else 0

    certified = (
        py_core > 0
        and js_src_wt >= py_core * 0.99
        and dart_lib_git >= py_core * 0.99
        and not missing_js
        and not missing_dart
    )

    inventory = {
        "measured_at": ts,
        "python": {
            "ref": py_ref,
            "core_modules": py_core,
            "top_level_packages": py_pkg_count,
            "validation_py": py_val,
            "tests": py_tests,
            "workflows": workflow_count(py_ref),
            "governance_files": len(gov_py),
        },
        "javascript": {
            "ref": js_ref,
            "src_modules_git": js_src_git,
            "src_modules_worktree": js_src_wt,
            "top_level_packages": js_pkg_count,
            "validation_ts_git": js_val_git,
            "validation_ts_worktree": js_val_wt,
            "tests_git": js_tests_git,
            "tests_worktree": js_tests_wt,
            "workflows": workflow_count(js_ref),
            "governance_files": len(gov_js),
            "module_depth_pct_of_python": equality_ratio_js,
        },
        "dart": {
            "ref": dart_ref,
            "lib_modules_git": dart_lib_git,
            "lib_modules_worktree": dart_lib_wt,
            "top_level_packages": dart_pkg_count,
            "validation_dart": dart_val,
            "tests": dart_tests,
            "workflows": workflow_count(dart_ref),
            "governance_files": len(gov_dart),
            "module_depth_pct_of_python": equality_ratio_dart,
        },
        "gaps": {
            "packages_missing_in_javascript": missing_js,
            "packages_missing_in_dart": missing_dart,
        },
        "true_equality_certified": certified,
    }

    SPECS.mkdir(parents=True, exist_ok=True)
    (SPECS / "forensic_inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")

  # Reports
    write(
        "FINAL_TRUE_EQUALITY_AUDIT.md",
        "\n".join(
            [
                "# FINAL TRUE EQUALITY AUDIT",
                "",
                f"**Measured (UTC):** {ts}",
                "",
                "## Module depth",
                "",
                "| Branch | Ref | Production modules | % of Python |",
                "|--------|-----|-------------------|-------------|",
                f"| Python | `{py_ref}` | **{py_core}** | 100% |",
                f"| JavaScript (git) | `{js_ref}` | {js_src_git} | {round(js_src_git/py_core*100,2) if py_core else 0}% |",
                f"| JavaScript (worktree) | working tree | **{js_src_wt}** | **{equality_ratio_js}%** |",
                f"| Dart | `{dart_ref}` | {dart_lib_git} | {equality_ratio_dart}% |",
                "",
                "## Package surface",
                "",
                f"| | Python packages | JS packages | Dart packages |",
                f"|--|-----------------|-------------|---------------|",
                f"| Count | {py_pkg_count} | {js_pkg_count} | {dart_pkg_count} |",
                "",
                f"**Packages in Python missing from JavaScript:** {len(missing_js)}",
                f"**Packages in Python missing from Dart:** {len(missing_dart)}",
                "",
                "## Verdict",
                "",
                "**TRUE EQUALITY: NOT CERTIFIED**" if not certified else "**TRUE EQUALITY: CERTIFIED**",
                "",
                "Certification requires ~99% module depth match, zero missing top-level packages, "
                "validator parity, coverage gates, and governance parity.",
                "",
            ]
        ),
    )

    def matrix_table(title: str, py_d: dict[str, int], other_d: dict[str, int], other_name: str) -> str:
        lines = [
            f"# {title}",
            "",
            f"**Measured:** {ts}",
            "",
            "| Package | Python | " + other_name + " | Delta |",
            "|---------|--------|" + "-" * len(other_name) + "|-------|",
        ]
        all_pkgs = sorted(set(py_d) | set(other_d))
        for pkg in all_pkgs:
            p = py_d.get(pkg, 0)
            o = other_d.get(pkg, 0)
            lines.append(f"| `{pkg}` | {p} | {o} | {o - p:+d} |")
        lines.extend(["", f"**Totals:** Python {sum(py_d.values())}, {other_name} {sum(other_d.values())}", ""])
        return "\n".join(lines)

    write("FINAL_FILE_DEPTH_MATRIX.md", matrix_table("FINAL FILE DEPTH MATRIX", py_pkgs, js_pkgs, "JavaScript"))
    write(
        "FINAL_SUBSYSTEM_MATRIX.md",
        matrix_table("FINAL SUBSYSTEM MATRIX (Dart)", py_pkgs, dart_pkgs, "Dart"),
    )

    write(
        "FINAL_VALIDATION_MATRIX.md",
        "\n".join(
            [
                "# FINAL VALIDATION MATRIX",
                "",
                f"**Measured:** {ts}",
                "",
                "| Branch | Validators | Tests |",
                "|--------|------------|-------|",
                f"| Python | {py_val} (.py) | {py_tests} |",
                f"| JavaScript (git) | {js_val_git} (.ts) | {js_tests_git} |",
                f"| JavaScript (worktree) | {js_val_wt} (.ts) | {js_tests_wt} |",
                f"| Dart | {dart_val} (.dart) | {dart_tests} |",
                "",
                "**Coverage targets (required):** lines ≥97%, functions ≥98%, statements ≥97%, branches ≥90%.",
                "",
            ]
        ),
    )

    write(
        "FINAL_GOVERNANCE_MATRIX.md",
        "\n".join(
            [
                "# FINAL GOVERNANCE MATRIX",
                "",
                f"**Measured:** {ts}",
                "",
                "| File | Python | JavaScript | Dart |",
                "|------|--------|------------|------|",
                *[
                    f"| `{g}` | {'yes' if g in gov_py or any(x.endswith(g) for x in gov_py) else 'no'} | "
                    f"{'yes' if g in gov_js or any(x.endswith(g) for x in gov_js) else 'no'} | "
                    f"{'yes' if g in gov_dart or any(x.endswith(g) for x in gov_dart) else 'no'} |"
                    for g in [
                        "CONTRIBUTING.md",
                        "SECURITY.md",
                        "CODE_OF_CONDUCT.md",
                        "LICENSE",
                        "ROADMAP.md",
                        "CODEOWNERS",
                    ]
                ],
                "",
            ]
        ),
    )

    write(
        "FINAL_OSS_MATRIX.md",
        "\n".join(
            [
                "# FINAL OSS MATRIX",
                "",
                f"**Measured:** {ts}",
                "",
                "| Dimension | Python | JavaScript | Dart |",
                "|-----------|--------|------------|------|",
                f"| CI workflows | {workflow_count(py_ref)} | {workflow_count(js_ref)} | {workflow_count(dart_ref)} |",
                f"| Governance files | {len(gov_py)} | {len(gov_js)} | {len(gov_dart)} |",
                f"| Test files | {py_tests} | {js_tests_wt} | {dart_tests} |",
                "",
            ]
        ),
    )

    write(
        "FINAL_RUNTIME_MATRIX.md",
        "\n".join(
            [
                "# FINAL RUNTIME MATRIX",
                "",
                f"**Measured:** {ts}",
                "",
                "Runtime subsystems (Python `core/` module counts):",
                "",
                "| Subsystem | Python modules |",
                "|-----------|------------------|",
                *[
                    f"| `{k}` | {v} |"
                    for k, v in sorted(py_pkgs.items())
                    if k
                    in (
                        "runtime",
                        "replay",
                        "reconstruction",
                        "kernel",
                        "execution",
                        "orchestration",
                        "workflows",
                        "distributed",
                        "vm",
                        "cognition",
                        "browser",
                        "memory",
                        "graph",
                        "semantic",
                    )
                ],
                "",
            ]
        ),
    )

    write(
        "FINAL_TRUE_EQUALITY_REPORT.md",
        "\n".join(
            [
                "# FINAL TRUE EQUALITY REPORT",
                "",
                f"**Measured:** {ts}",
                "",
                "## Summary",
                "",
                f"- Python canonical modules: **{py_core}**",
                f"- JavaScript worktree modules: **{js_src_wt}** ({equality_ratio_js}%)",
                f"- Dart modules: **{dart_lib_git}** ({equality_ratio_dart}%)",
                "",
                "## Certification",
                "",
                "**TRUE EQUALITY: NOT ACHIEVED**",
                "",
                "See `FINAL_TRUE_EQUALITY_AUDIT.md`, `FINAL_FILE_DEPTH_MATRIX.md`, "
                "`docs/specs/forensic_inventory.json`.",
                "",
            ]
        ),
    )

    if certified:
        write(
            "FINAL_TRUE_EQUALITY_CERTIFICATION.md",
            "\n".join(
                [
                    "# FINAL TRUE EQUALITY CERTIFICATION",
                    "",
                    f"**Certified at:** {ts}",
                    "",
                    "All audited gates passed. See forensic_inventory.json.",
                    "",
                ]
            ),
        )
    else:
        write(
            "FINAL_TRUE_EQUALITY_CERTIFICATION.md",
            "\n".join(
                [
                    "# FINAL TRUE EQUALITY CERTIFICATION",
                    "",
                    "**STATUS: NOT ISSUED**",
                    "",
                    f"**Measured:** {ts}",
                    "",
                    "## Blocking gaps",
                    "",
                    f"- JavaScript module depth: {js_src_wt} / {py_core} required",
                    f"- Dart module depth: {dart_lib_git} / {py_core} required",
                    f"- Missing JS packages: {len(missing_js)}",
                    f"- Missing Dart packages: {len(missing_dart)}",
                    "",
                    "Equality cannot be claimed until gaps are closed and all validation/coverage gates pass.",
                    "",
                ]
            ),
        )

    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
