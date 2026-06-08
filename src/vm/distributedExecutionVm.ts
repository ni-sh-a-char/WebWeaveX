import { synchronizeDistributedCognition } from "../distributed/distributedCognitionSync.js";

export function executeDistributedVm(
  nodes: Array<Record<string, unknown>>,
  events: Array<Record<string, unknown>>,
): Record<string, unknown> {
  const sync = synchronizeDistributedCognition(nodes, events);
  return { ...sync, vm: "distributed", bounded: true };
}
