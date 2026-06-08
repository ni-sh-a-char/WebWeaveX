/**
 * Run all differential equivalence validators (Python canonical vectors → JS execution).
 */
import { execSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const vectorsDir = join(root, "validation/vectors");

const VALIDATORS = [
  "validateGraphEquivalence.ts",
  "validateRuntimeEquivalence.ts",
  "validateMemoryEquivalence.ts",
  "validateReconstructionEquivalence.ts",
  "validateReplayEquivalence.ts",
  "validateSemanticEquivalence.ts",
  "validateOntologyEquivalence.ts",
  "validateVmEquivalence.ts",
  "validateDistributedEquivalence.ts",
  "validateWorkflowEquivalence.ts",
  "validateRepositoryEquivalence.ts",
  "validateParserEquivalence.ts",
  "validateBrowserEquivalence.ts",
  "validateContinuationEquivalence.ts",
];

if (!existsSync(join(vectorsDir, "graph_vectors", "canonical.json"))) {
  console.error("Canonical vectors missing. Run:");
  console.error("  python tools/runtime_vectors/generate_canonical_vectors.py");
  process.exit(1);
}

import { writeDifferentialReport, type DifferentialSummary } from "./writeDifferentialReport.js";

let failed = 0;
const familyResults: DifferentialSummary["families"] = [];
console.log("# Differential equivalence suite\n");
for (const name of VALIDATORS) {
  const path = join(root, "validation/differential", name);
  try {
    execSync(`npx tsx ${path}`, { stdio: "inherit", cwd: root });
    familyResults.push({ family: name, pass: true, failed_ids: [] });
  } catch {
    failed += 1;
    familyResults.push({ family: name, pass: false, failed_ids: ["see log"] });
  }
}

const summary: DifferentialSummary = {
  measured_at: new Date().toISOString(),
  families_passed: familyResults.filter((f) => f.pass).length,
  families_failed: failed,
  probes_passed: 0,
  probes_failed: 0,
  families: familyResults,
};
writeDifferentialReport(summary);

if (failed > 0) {
  console.error(`\n${failed} differential validator(s) FAILED`);
  process.exit(1);
}
console.log("\n✅ All differential equivalence validators passed");
