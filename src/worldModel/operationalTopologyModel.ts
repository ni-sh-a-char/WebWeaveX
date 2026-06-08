import type { RuntimeGraph } from "../contracts/graphContracts.js";
import { graphFingerprint } from "../graph/runtimeGraph.js";

export function modelOperationalTopology(graph: RuntimeGraph): Record<string, unknown> {
  return {
    topology_id: graphFingerprint(graph),
    node_count: graph.nodes.length,
    edge_count: graph.edges.length,
    bounded: graph.bounded === true,
  };
}
