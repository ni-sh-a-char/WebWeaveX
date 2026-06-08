import {
  computeRuntimeFingerprint,
  graphFingerprint,
  validateRuntimeGraph,
} from "../../src/index.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

const graph = buildRuntimeGraph({
  nodes: [{ id: "b" }, { id: "a" }],
  edges: [],
});
const v = validateRuntimeGraph(graph);
const results = {
  graph_match: v.valid === true,
  fingerprint_match: computeRuntimeFingerprint(graph) === graphFingerprint(graph),
  deterministic: computeRuntimeFingerprint(graph) === computeRuntimeFingerprint(graph),
};
const allOk = Object.values(results).every(Boolean);
console.log(allOk ? "PASS" : "FAIL", results);
if (!allOk) process.exit(1);
