import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";
import { graphFingerprint } from "./runtimeGraph.js";

export function reasonTopology(graph: RuntimeGraph): Record<string, unknown> {
  return {
    topology_id: graphFingerprint(graph),
    node_count: graph.nodes.length,
    edge_count: graph.edges.length,
    bounded: true,
  };
}

export function diffRuntimeGraphs(
  left: RuntimeGraph,
  right: RuntimeGraph,
): Record<string, unknown> {
  const leftIds = new Set(left.nodes.map((n) => n.id));
  const added = right.nodes.filter((n) => !leftIds.has(n.id));
  const removed = left.nodes.filter((n) => !right.nodes.some((r) => r.id === n.id));
  return {
    added,
    removed,
    bounded: true,
    diff_id: computeDeterministicHash({ added: added.length, removed: removed.length }),
  };
}

export function buildGraphCognitionIndex(graph: RuntimeGraph): Record<string, unknown> {
  return {
    index_id: computeDeterministicHash({ fp: graphFingerprint(graph), n: graph.nodes.length }),
    fingerprint: graphFingerprint(graph),
    bounded: true,
  };
}

export function analyzeGraphContradictions(graph: RuntimeGraph): Record<string, unknown> {
  const edgeTypes = graph.edges.map((e) => e.type);
  const dupes = edgeTypes.length - new Set(edgeTypes).size;
  return { contradictory_edges: dupes, bounded: true };
}

export function reconcileGraphs(graphs: RuntimeGraph[]): RuntimeGraph {
  const nodes = graphs.flatMap((g, gi) =>
    g.nodes.map((n, ni) => ({ ...n, id: `g${gi}:${String(n.id ?? ni)}` })),
  );
  const edges = graphs.flatMap((g) => g.edges);
  return RuntimeGraphContract.normalize({ nodes, edges, bounded: true });
}

export const reconstructGraph = reconcileGraphs;
export const compressGraph = (g: RuntimeGraph): RuntimeGraph => g;
export const exportGraph = graphFingerprint;
