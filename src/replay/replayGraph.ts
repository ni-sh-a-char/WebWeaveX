import stringify from "fast-json-stable-stringify";
import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { computeKaalkaHash } from "../crypto/kaalkaRuntime.js";

export function graphReplayHash(graph: RuntimeGraph): string {
  const normalized = RuntimeGraphContract.normalize(graph);
  return computeKaalkaHash(stringify({ nodes: normalized.nodes, edges: normalized.edges }));
}

export function replayRuntimeGraph(graph: RuntimeGraph): RuntimeGraph {
  return RuntimeGraphContract.normalize(JSON.parse(stringify(graph)) as RuntimeGraph);
}

export function validateGraphReplayEquivalence(
  original: RuntimeGraph,
  replayed: RuntimeGraph,
): { equivalent: boolean; graph_hash: string; replay_hash: string; bounded: boolean } {
  const graph_hash = graphReplayHash(original);
  const replay_hash = graphReplayHash(replayed);
  return {
    equivalent: graph_hash === replay_hash,
    graph_hash,
    replay_hash,
    bounded: true,
  };
}
