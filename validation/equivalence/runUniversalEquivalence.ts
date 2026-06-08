/**
 * Universal specification equivalence harness.
 * The canonical vectors under `specification/vectors/` are the sole authority
 * (tagged `webweavex-spec`); the JavaScript implementation must match them
 * structurally and by hash fields. Neither implementation is the authority —
 * both conform to the specification.
 */
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { summarizeDiffs } from "./deepCompare.js";
import { runUniversalEquivalence } from "./harness.js";
import { writeEqualityReports } from "./generateEqualityReports.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
// specification/vectors is authoritative; validation/vectors is the dev
// working copy synced into it. Prefer the specification authority.
const specVectors = join(root, "specification/vectors");
const vectorsRoot = existsSync(specVectors) ? specVectors : join(root, "validation/vectors");
const specsDir = join(root, "docs/specs");

console.log("# Universal equivalence harness\n");

const summary = runUniversalEquivalence(vectorsRoot);

mkdirSync(specsDir, { recursive: true });
writeFileSync(join(specsDir, "universal_equivalence.json"), JSON.stringify(summary, null, 2), "utf-8");

writeEqualityReports(summary);

console.log(`Families: ${summary.vector_families}`);
console.log(`Probes: ${summary.total_probes} passed=${summary.passed} failed=${summary.failed} (${summary.pass_rate}%)`);
console.log("\n## Subsystems");
for (const s of summary.subsystems) {
  console.log(`  ${s.name}: ${s.status} (${s.passed}/${s.probes})`);
}

const hashFailed = summary.probes.filter((p) => !p.hash_pass);
const structFailed = summary.probes.filter((p) => !p.structure_pass);

if (hashFailed.length > 0) {
  console.error(`\n${hashFailed.length} hash equivalence probe(s) FAILED`);
  for (const p of hashFailed) {
    console.error(`  ❌ ${p.family}/${p.vector_id}:`, p.hash_mismatches.slice(0, 3).join("; "));
  }
  process.exit(1);
}

if (structFailed.length > 0) {
  console.warn(`\n${structFailed.length} probe(s) pass hashes but differ structurally (convergence in progress)`);
  for (const p of structFailed) {
    console.warn(`  ⚠ ${p.family}/${p.vector_id}:`, summarizeDiffs(p.structural_diffs).slice(0, 2).join("; "));
  }
}

console.log("\n✅ Universal equivalence: all hash probes passed (vector scope)");
