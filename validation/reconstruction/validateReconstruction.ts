import { buildRuntimeGraph, reconstructRuntime } from "../../src/index.js";

const graph = buildRuntimeGraph({ a: 1 });
const extraction = { unified_runtime_graph: graph, graph };
const r1 = reconstructRuntime({ extraction });
const r2 = reconstructRuntime({ extraction });
const id1 = (r1.runtime as Record<string, unknown>).runtime_id;
const id2 = (r2.runtime as Record<string, unknown>).runtime_id;
const results = {
  reconstruction_match: id1 === id2,
  bounded: r1.bounded === true,
};
const allOk = Object.values(results).every(Boolean);
console.log(allOk ? "PASS" : "FAIL", results);
if (!allOk) process.exit(1);
