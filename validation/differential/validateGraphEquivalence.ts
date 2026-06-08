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
  const sources = vector.input.sources as Record<string, unknown>;
  const graph = buildRuntimeGraph(sources);
  const output = graph as unknown as Record<string, unknown>;
  return {
    output,
    hashes: {
      graph_hash: parityGraphHash(graph),
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("graph_vectors", run);
printFamilyReport(report, "Graph equivalence");
exitOnReports([report]);
