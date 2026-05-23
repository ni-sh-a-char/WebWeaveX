import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { graphReplayHash, replayRuntimeGraph } from "../replay/replayGraph.js";

export function replayGraphLineage(graph: RuntimeGraph): {
  replayed: RuntimeGraph;
  lineage_hash: string;
  bounded: boolean;
} {
  const replayed = replayRuntimeGraph(graph);
  return {
    replayed,
    lineage_hash: graphReplayHash(replayed),
    bounded: true,
  };
}

export function mergeGraphReplay(base: RuntimeGraph, overlay: RuntimeGraph): RuntimeGraph {
  const b = RuntimeGraphContract.normalize(base);
  const o = RuntimeGraphContract.normalize(overlay);
  return RuntimeGraphContract.normalize({
    nodes: [...b.nodes, ...o.nodes],
    edges: [...b.edges, ...o.edges],
    bounded: true,
  });
}
