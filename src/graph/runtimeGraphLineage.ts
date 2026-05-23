import { computeGraphLineageFingerprint } from "./runtimeGraphFingerprint.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function buildRuntimeGraphLineage(graphs: RuntimeGraph[]): Record<string, unknown> {
  const fp = computeGraphLineageFingerprint(graphs);
  return {
    lineage_fingerprint: fp.lineage_fingerprint,
    graph_count: fp.count,
    bounded: true,
  };
}
