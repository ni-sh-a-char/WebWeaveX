import {
  RuntimeGraphContract,
  type RuntimeGraph,
  type RuntimeNode,
  type RuntimeEdge,
} from "../contracts/graphContracts.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";

export type MemoryGraphEntity = { id: string; type: string; relations: string[] };
export type RuntimeMemoryGraph = {
  entities: MemoryGraphEntity[];
  relations: Array<{ from: string; to: string; type: string }>;
  graph_fingerprint: string;
  bounded: boolean;
};

export function buildRuntimeMemoryGraph(
  graph: RuntimeGraph,
  history: unknown[] = [],
): RuntimeMemoryGraph {
  const normalized = RuntimeGraphContract.normalize(graph) as {
    nodes: RuntimeNode[];
    edges: RuntimeEdge[];
  };
  const entities: MemoryGraphEntity[] = normalized.nodes.map((n: RuntimeNode) => ({
    id: String(n.id),
    type: String(n.type ?? "node"),
    relations: normalized.edges
      .filter((e: RuntimeEdge) => e.source === n.id || e.from === n.id)
      .map((e: RuntimeEdge) => String(e.target ?? e.to)),
  }));
  const relations = normalized.edges.map((e: RuntimeEdge) => ({
    from: String(e.source ?? e.from),
    to: String(e.target ?? e.to),
    type: String(e.type ?? "link"),
  }));
  return {
    entities,
    relations,
    graph_fingerprint: computeKaalkaHashPayload({ entities, relations, history_len: history.length }),
    bounded: true,
  };
}
