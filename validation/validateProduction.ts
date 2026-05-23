/**
 * Production smoke validation — writes report to docs/archive only.
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { encryptValue } from "../src/crypto/kaalkaRuntime.js";
import { validateReplayEquivalence } from "../src/replay/replayEquivalence.js";
import { buildRuntimeGraph } from "../src/graph/runtimeGraph.js";
import { extractWeb } from "../src/browser/extractWeb.js";
import { computeGlobalRuntimeFingerprint } from "../src/determinism/globalRuntimeFingerprint.js";
import { reconstructRuntime } from "../src/reconstruction/reconstructRuntime.js";
import { buildRuntimeMemory } from "../src/memory/runtimeMemory.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const archiveDir = join(root, "docs/archive");

async function main(): Promise<void> {
  mkdirSync(archiveDir, { recursive: true });

  const enc = encryptValue("probe", "k");
  const graph = buildRuntimeGraph({ probe: 1 });
  const sample = {
    bounded: true,
    unified_runtime_graph: graph,
    browser_ir: { runtime_identity: "x" },
    pipeline_hash: "ph",
  };
  const replay = validateReplayEquivalence(sample, structuredClone(sample));
  const fp = computeGlobalRuntimeFingerprint(sample, graph);
  const rebuilt = reconstructRuntime({ extraction: sample });
  const mem = buildRuntimeMemory(graph);

  let extractOk = false;
  let nodeCount = 0;
  try {
    const ex = await extractWeb("https://example.com");
    extractOk = ex.bounded === true;
    nodeCount = ex.unified_runtime_graph?.nodes?.length ?? 0;
  } catch {
    extractOk = false;
  }

  const report = [
    "# Production Validation Report",
    "",
    `**Generated:** ${new Date().toISOString()}`,
    "",
    "| Check | Result |",
    "|-------|--------|",
    `| Kaalka deterministic encrypt | ${enc.deterministic} |`,
    `| Replay equivalence | ${replay.equivalent} |`,
    `| Global fingerprint | ${fp.slice(0, 16)}… |`,
    `| Reconstruction runtime_id | ${(rebuilt.runtime as Record<string, string>).runtime_id?.slice(0, 16)}… |`,
    `| Memory stable_hash | ${Boolean(mem.stable_hash)} |`,
    `| extractWeb (example.com) | ${extractOk} (${nodeCount} nodes) |`,
  ].join("\n");

  writeFileSync(join(archiveDir, "FINAL_REAL_WORLD_VALIDATION_REPORT.md"), report);
  console.log(report);
}

main();
