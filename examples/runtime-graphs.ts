/**
 * Runtime graphs — merge heterogeneous runtime IRs into one canonical,
 * deterministic graph and fingerprint it.
 *   npx tsx examples/runtime-graphs.ts
 */
import { buildRuntimeGraph, computeGlobalRuntimeFingerprint } from "webweavex";

const graph = buildRuntimeGraph([
  { ir: "browser", nodes: [{ id: "page" }, { id: "form" }], edges: [{ from: "page", to: "form" }] },
  { ir: "memory", nodes: [{ id: "session" }], edges: [] },
]);

console.log("nodes:", graph.nodes.length, "edges:", graph.edges.length);
console.log("fingerprint:", computeGlobalRuntimeFingerprint({ graph }, graph));
