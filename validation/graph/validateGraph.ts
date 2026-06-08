import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import {
  analyzeGraphContradictions,
  buildGraphCognitionIndex,
  diffRuntimeGraphs,
  reasonTopology,
  reconcileGraphs,
} from "../../src/graph/graphIntelligence.js";

const g1 = buildRuntimeGraph({ a: { x: 1 } });
const g2 = buildRuntimeGraph({ b: { y: 2 } });

const results = {
  topology: reasonTopology(g1).bounded === true,
  diff: diffRuntimeGraphs(g1, g2).bounded === true,
  index: Boolean(buildGraphCognitionIndex(g1).index_id),
  reconcile: reconcileGraphs([g1, g2]).nodes.length >= 2,
  contradictions: analyzeGraphContradictions(g1).bounded === true,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
