import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function synchronizeDistributedCognition(
  nodes: Array<Record<string, unknown>>,
  events: Array<Record<string, unknown>>,
): Record<string, unknown> {
  const healed = nodes.flatMap((n) => {
    const mem = ((n.adaptive_runtime as Record<string, unknown>)?.memory as Record<string, unknown>) ?? {};
    const selectors = (mem.healed_selectors as Record<string, unknown>) ?? {};
    return Object.keys(selectors);
  });
  return {
    synchronized: true,
    node_count: nodes.length,
    event_count: events.length,
    healed_selectors: healed,
    sync_id: computeDeterministicHash({ nodes, events }),
    bounded: true,
  };
}

export function federateSemanticMemory(
  shards: Array<Record<string, unknown>>,
): Record<string, unknown> {
  return {
    shard_count: shards.length,
    federated: true,
    bounded: true,
    federation_id: computeDeterministicHash({ shards }),
  };
}
