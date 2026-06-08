import { modelOperationalTopology } from "./operationalTopologyModel.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function buildDistributedTopologyWorldState(
  shards: RuntimeGraph[],
): Record<string, unknown> {
  const topologies = shards.map((g) => modelOperationalTopology(g));
  return {
    shard_count: shards.length,
    topologies,
    bounded: true,
  };
}
