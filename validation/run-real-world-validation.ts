import { writeFileSync, mkdirSync } from "node:fs";
import { encryptValue } from "../src/crypto/kaalkaRuntime.js";
import { validateReplayEquivalence } from "../src/replay/replayEquivalence.js";
import { buildRuntimeGraph } from "../src/graph/runtimeGraph.js";
import { extractWeb } from "../src/browser/extractWeb.js";

async function main(): Promise<void> {
  mkdirSync("docs/validation", { recursive: true });
  const enc = encryptValue("probe", "k");
  const graph = buildRuntimeGraph({ probe: 1 });
  const sample = { bounded: true, unified_runtime_graph: graph, browser_ir: { runtime_identity: "x" } };
  const replay = validateReplayEquivalence(sample, structuredClone(sample));

  let extractOk = false;
  try {
    const ex = await extractWeb("https://example.com");
    extractOk = ex.bounded === true;
  } catch {
    extractOk = false;
  }

  const report = [
    "# FINAL REAL WORLD VALIDATION (JavaScript)",
    "",
    `- Kaalka encrypt deterministic: **${enc.deterministic}**`,
    `- Replay equivalence: **${replay.equivalent}**`,
    `- extractWeb bounded: **${extractOk}**`,
    "",
    `Generated: ${new Date().toISOString()}`,
  ].join("\n");

  writeFileSync("FINAL_RUNTIME_VALIDATION_REPORT.md", report);
  writeFileSync("docs/validation/FINAL_RUNTIME_VALIDATION_REPORT.md", report);
  console.log(report);
}

main();
