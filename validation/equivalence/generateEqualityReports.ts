import { writeFileSync, mkdirSync, readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import type { SubsystemSummary, UniversalEquivalenceSummary } from "./types.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const archive = join(root, "docs/archive");
const specs = join(root, "docs/specs");

/* ------------------------------------------------------------------ */
/* measured gates — every claim below is read from an execution        */
/* artifact or scanned from the working tree at generation time        */
/* ------------------------------------------------------------------ */

type Gate = { name: string; pass: boolean; detail: string };

function moduleMatrixGate(): Gate {
  const p = join(specs, "implementation_equality_matrix.json");
  if (!existsSync(p)) {
    return { name: "Generated-port behavioral proof", pass: false, detail: "implementation_equality_matrix.json missing — matrix not yet run" };
  }
  const m = JSON.parse(readFileSync(p, "utf-8")) as {
    mapped_pairs: number;
    classification_counts: Record<string, number>;
  };
  const counts = m.classification_counts ?? {};
  const equal = counts["EQUAL"] ?? 0;
  const other = Object.entries(counts).filter(([k]) => k !== "EQUAL");
  const pass = equal === m.mapped_pairs && other.every(([, v]) => v === 0);
  const otherStr = other.length ? `, ${other.map(([k, v]) => `${k}=${v}`).join(", ")}` : "";
  return {
    name: "Generated-port behavioral proof",
    pass,
    detail: `EQUAL=${equal}/${m.mapped_pairs}${otherStr} (docs/specs/implementation_equality_matrix.json)`,
  };
}

function tsNocheckGate(): Gate {
  let count = 0;
  const scan = (dir: string): void => {
    for (const entry of readdirSync(dir)) {
      const p = join(dir, entry);
      if (statSync(p).isDirectory()) {
        scan(p);
      } else if (entry.endsWith(".ts") && /^\s*\/\/\s*@ts-nocheck/m.test(readFileSync(p, "utf-8"))) {
        count += 1;
      }
    }
  };
  for (const d of ["src", "tests"]) scan(join(root, d));
  return { name: "@ts-nocheck count", pass: count === 0, detail: `${count} files (scanned src/, tests/)` };
}

function coverageGate(): Gate {
  const p = join(root, "coverage", "coverage-summary.json");
  if (!existsSync(p)) {
    return { name: "Coverage thresholds", pass: false, detail: "coverage/coverage-summary.json missing — run `npx vitest run --coverage`" };
  }
  const total = (JSON.parse(readFileSync(p, "utf-8")) as { total: Record<string, { pct: number }> }).total;
  const targets: Array<[string, number]> = [["lines", 98], ["functions", 98], ["branches", 95], ["statements", 98]];
  const pass = targets.every(([k, t]) => (total[k]?.pct ?? 0) >= t);
  return {
    name: "Coverage thresholds",
    pass,
    detail: targets.map(([k, t]) => `${k} ${total[k]?.pct ?? 0}% (≥${t}%)`).join(", "),
  };
}

function realWorldGate(): Gate {
  const p = join(specs, "real_world_probe.json");
  if (!existsSync(p)) {
    return { name: "Real-world URL validation", pass: false, detail: "real_world_probe.json missing — run validate:realworld" };
  }
  const r = JSON.parse(readFileSync(p, "utf-8")) as {
    measured_at: string;
    urls_executed: number;
    match_pct: number;
    drift_pct: number;
    drift_threshold_pct: number;
    pass: boolean;
  };
  return {
    name: "Real-world URL validation",
    pass: r.pass === true,
    detail: `${r.urls_executed} URLs, match ${r.match_pct}%, drift ${r.drift_pct}% (≤${r.drift_threshold_pct}%), measured ${r.measured_at}`,
  };
}

/* ------------------------------------------------------------------ */
/* per-subsystem equality reports                                      */
/* ------------------------------------------------------------------ */

function subsystemBody(name: string, summary: SubsystemSummary, probes: UniversalEquivalenceSummary["probes"]): string {
  const related = probes.filter((p) =>
    ({
      runtime: ["runtime_vectors", "runtime_identity_vectors", "continuation_vectors"],
      memory: ["memory_vectors", "continuation_memory_vectors", "distributed_memory_vectors"],
      reconstruction: ["reconstruction_vectors"],
      semantic: ["semantic_vectors", "semantic_reconciliation_vectors"],
      ontology: ["ontology_vectors"],
      workflow: ["workflow_vectors", "workflow_graph_vectors"],
      distributed: ["distributed_vectors", "distributed_replay_vectors"],
      replay: ["replay_vectors"],
      vm: ["vm_vectors"],
      graph: ["graph_vectors", "browser_vectors"],
      extraction: ["orchestration_vectors", "parser_vectors"],
    } as Record<string, string[]>)[name]?.includes(p.family),
  );
  const failed = related.filter((p) => !p.pass);
  return [
    `# FINAL ${name.toUpperCase()} EQUALITY REPORT`,
    "",
    `**Measured:** ${new Date().toISOString()}`,
    "",
    `**Status:** ${summary.status}`,
    "",
    `| Probes | Passed | Failed | Pass rate |`,
    `|--------|--------|--------|-----------|`,
    `| ${summary.probes} | ${summary.passed} | ${summary.failed} | ${summary.pass_rate}% |`,
    "",
    "## Method",
    "",
    "Universal equivalence harness: execute JavaScript against the canonical specification vectors (specification/vectors, tagged webweavex-spec), deep structural compare + hash fields. Neither implementation is canonical; both conform to specification/.",
    "",
    ...(failed.length
      ? ["## Failures", "", ...failed.map((f) => `- \`${f.family}/${f.vector_id}\`: ${f.hash_mismatches.join("; ")}`), ""]
      : ["## Failures", "", "_None on probed vectors._", ""]),
    "",
    `**Certification:** ${summary.failed === 0 ? "PASS — all probed vectors equal" : "FAIL — divergent vectors listed above"}`,
    "",
  ].join("\n");
}

const REPORT_MAP: Record<string, string> = {
  runtime: "FINAL_RUNTIME_EQUALITY_REPORT.md",
  memory: "FINAL_MEMORY_EQUALITY_REPORT.md",
  reconstruction: "FINAL_RECONSTRUCTION_EQUALITY_REPORT.md",
  semantic: "FINAL_SEMANTIC_EQUALITY_REPORT.md",
  ontology: "FINAL_ONTOLOGY_EQUALITY_REPORT.md",
  workflow: "FINAL_WORKFLOW_EQUALITY_REPORT.md",
  distributed: "FINAL_DISTRIBUTED_EQUALITY_REPORT.md",
  vm: "FINAL_VM_EQUALITY_REPORT.md",
  replay: "FINAL_REPLAY_EQUALITY_REPORT.md",
  graph: "FINAL_GRAPH_EQUALITY_REPORT.md",
  extraction: "FINAL_EXTRACTION_EQUALITY_REPORT.md",
};

export function writeEqualityReports(summary: UniversalEquivalenceSummary): void {
  mkdirSync(archive, { recursive: true });
  for (const sub of summary.subsystems) {
    const file = REPORT_MAP[sub.name];
    if (file) {
      writeFileSync(join(archive, file), subsystemBody(sub.name, sub, summary.probes), "utf-8");
    }
  }

  const gates: Gate[] = [
    {
      name: "Universal equivalence harness",
      pass: summary.failed === 0,
      detail: `${summary.passed}/${summary.total_probes} probes passed across ${summary.vector_families} families`,
    },
    moduleMatrixGate(),
    tsNocheckGate(),
    coverageGate(),
    realWorldGate(),
  ];
  const allPass = gates.every((g) => g.pass);

  const cert = [
    "# FINAL TRUE EQUALITY CERTIFICATION",
    "",
    allPass ? "**TRUE**" : "**STATUS: NOT ISSUED**",
    "",
    `**Measured:** ${summary.measured_at}`,
    "",
    "## Universal equivalence harness",
    "",
    `| Metric | Value |`,
    `|--------|-------|`,
    `| Vector families | ${summary.vector_families} |`,
    `| Probes executed | ${summary.total_probes} |`,
    `| Passed | ${summary.passed} |`,
    `| Failed | ${summary.failed} |`,
    `| Pass rate | ${summary.pass_rate}% |`,
    "",
    "## Gates (measured at generation time)",
    "",
    "| Gate | Status | Evidence |",
    "|------|--------|----------|",
    ...gates.map((g) => `| ${g.name} | ${g.pass ? "PASS" : "FAIL"} | ${g.detail} |`),
    "",
    allPass
      ? "All gates above were measured from execution artifacts. TRUE EQUALITY ACHIEVED."
      : "One or more measured gates fail. TRUE EQUALITY NOT ACHIEVED. Convergence continues.",
    "",
  ].join("\n");

  writeFileSync(join(archive, "FINAL_TRUE_EQUALITY_CERTIFICATION.md"), cert, "utf-8");

  // real-world validation report — derived from the recorded execution
  // artifact written by validation/real_world/validateRealWorld.ts
  const rw = realWorldGate();
  writeFileSync(
    join(archive, "FINAL_REAL_WORLD_VALIDATION_REPORT.md"),
    [
      "# FINAL REAL-WORLD VALIDATION REPORT",
      "",
      `**Status: ${rw.pass ? "PASS" : "FAIL"}**`,
      "",
      `Evidence: ${rw.detail}`,
      "",
      "Source artifact: `docs/specs/real_world_probe.json` (written by `validation/real_world/validateRealWorld.ts`).",
      "See `docs/archive/FINAL_REAL_WORLD_CERTIFICATION.md` for the full metric table.",
      "",
    ].join("\n"),
    "utf-8",
  );

  // inspection-derived reports: every line below checks the working tree
  const present = (rel: string): string => `- \`${rel}\`: ${existsSync(join(root, rel)) ? "present" : "MISSING"}`;
  const governanceFiles = ["GOVERNANCE.md", "MAINTAINERS.md", "CODEOWNERS", "SUPPORT.md", "RELEASE.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE"];
  writeFileSync(
    join(archive, "FINAL_GOVERNANCE_EQUALITY_REPORT.md"),
    [
      "# FINAL GOVERNANCE EQUALITY REPORT",
      "",
      `**Measured:** ${summary.measured_at}`,
      "",
      `**Status: ${governanceFiles.every((f) => existsSync(join(root, f))) ? "PASS" : "INCOMPLETE"}**`,
      "",
      "Repository governance files (verified by inspection at generation time):",
      "",
      ...governanceFiles.map(present),
      "",
    ].join("\n"),
    "utf-8",
  );
  const securityFiles = [".github/workflows/security.yml", "SECURITY.md", "src/security/urlValidator.ts"];
  writeFileSync(
    join(archive, "FINAL_SECURITY_EQUALITY_REPORT.md"),
    [
      "# FINAL SECURITY EQUALITY REPORT",
      "",
      `**Measured:** ${summary.measured_at}`,
      "",
      `**Status: ${securityFiles.every((f) => existsSync(join(root, f))) ? "PASS" : "INCOMPLETE"}**`,
      "",
      "Security surface (verified by inspection at generation time):",
      "",
      ...securityFiles.map(present),
      "",
      "Runtime-authority audits (no Python invocation in the JS runtime, no",
      "Node invocation in the Python runtime) are recorded in",
      "`docs/archive/FINAL_JS_RELEASE_CERTIFICATION.md`.",
      "",
    ].join("\n"),
    "utf-8",
  );
  writeFileSync(
    join(archive, "FINAL_PERFORMANCE_EQUALITY_REPORT.md"),
    [
      "# FINAL PERFORMANCE EQUALITY REPORT",
      "",
      `**Measured:** ${summary.measured_at}`,
      "",
      `**Status: ${existsSync(join(root, ".github/workflows/benchmark.yml")) ? "TRACKED" : "INCOMPLETE"}**`,
      "",
      present(".github/workflows/benchmark.yml"),
      "",
      "Cross-language wall-clock performance parity is not a behavioral",
      "certification gate; behavioral equality gates are listed in",
      "`FINAL_TRUE_EQUALITY_CERTIFICATION.md`.",
      "",
    ].join("\n"),
    "utf-8",
  );
  writeFileSync(
    join(archive, "FINAL_RELEASE_READINESS_REPORT.md"),
    [
      "# FINAL RELEASE READINESS REPORT",
      "",
      `**Measured:** ${summary.measured_at}`,
      "",
      `**Status: ${allPass ? "READY" : "NOT READY"}**`,
      "",
      "| Gate | Status | Evidence |",
      "|------|--------|----------|",
      ...gates.map((g) => `| ${g.name} | ${g.pass ? "PASS" : "FAIL"} | ${g.detail} |`),
      "",
      "Packaging and npm-product gates are recorded in",
      "`docs/archive/FINAL_JS_RELEASE_CERTIFICATION.md` and",
      "`docs/archive/FINAL_NPM_READINESS_REPORT.md`.",
      "",
    ].join("\n"),
    "utf-8",
  );

  const audit = [
    "# FINAL TRUE EQUALITY AUDIT",
    "",
    `**Measured:** ${summary.measured_at}`,
    "",
    `**STATUS: ${allPass ? "TRUE EQUALITY ACHIEVED" : "TRUE EQUALITY NOT ACHIEVED"}**`,
    "",
    "## Subsystem matrix",
    "",
    "| Subsystem | Probes | Pass rate | Status |",
    "|-----------|--------|-----------|--------|",
    ...summary.subsystems.map(
      (s) => `| ${s.name} | ${s.probes} | ${s.pass_rate}% | ${s.status} |`,
    ),
    "",
    "## Gates",
    "",
    "| Gate | Status | Evidence |",
    "|------|--------|----------|",
    ...gates.map((g) => `| ${g.name} | ${g.pass ? "PASS" : "FAIL"} | ${g.detail} |`),
    "",
    "## Harness",
    "",
    "Run: `npm run validate:equivalence`",
    "",
    "specification/ canonical vectors → JavaScript execution → deep structural compare + hash parity (specification/ is the sole authority).",
    "",
  ].join("\n");

  writeFileSync(join(archive, "FINAL_TRUE_EQUALITY_AUDIT.md"), audit, "utf-8");
}
