import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import {
  fingerprint,
  parityGraphHash,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const url = String(vector.input.url ?? "https://example.com");
  const graph = buildRuntimeGraph({
    browser: { url, dom_hash: "abc" },
  });
  const output = { graph: graph as unknown as Record<string, unknown>, bounded: true };
  return {
    output,
    hashes: {
      graph_hash: parityGraphHash(graph),
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("browser_vectors", run);
printFamilyReport(report, "Browser equivalence");
exitOnReports([report]);
