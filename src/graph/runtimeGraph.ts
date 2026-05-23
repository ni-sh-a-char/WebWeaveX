import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHash.js";

export function buildRuntimeGraph(sources: Record<string, unknown>): RuntimeGraph {
  const nodes: RuntimeGraph["nodes"] = [];
  const edges: RuntimeGraph["edges"] = [];
  let idx = 0;
  for (const [kind, payload] of Object.entries(sources).sort(([a], [b]) => a.localeCompare(b))) {
    nodes.push({ id: `node:${kind}:${idx}`, type: kind, payload });
    idx += 1;
  }
  if (nodes.length > 1) {
    for (let i = 1; i < nodes.length; i++) {
      edges.push({
        source: nodes[0]!.id as string,
        target: nodes[i]!.id as string,
        type: "runtime_link",
      });
    }
  }
  return RuntimeGraphContract.normalize({ nodes, edges, bounded: true });
}

export function queryRuntimeGraph(graph: RuntimeGraph, nodeType?: string): RuntimeGraph {
  const g = RuntimeGraphContract.normalize(graph);
  if (!nodeType) return g;
  return RuntimeGraphContract.normalize({
    nodes: g.nodes.filter((n) => n.type === nodeType),
    edges: g.edges,
    bounded: true,
  });
}

export function graphFingerprint(graph: RuntimeGraph): string {
  return computeKaalkaHashPayload(RuntimeGraphContract.normalize(graph));
}
