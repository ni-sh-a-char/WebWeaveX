import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";
import { graphFingerprint } from "./runtimeGraph.js";

export function computeGraphLineageFingerprint(
  graphs: RuntimeGraph[],
): { lineage_fingerprint: string; count: number; bounded: boolean } {
  const hashes = graphs.map((g) => graphFingerprint(RuntimeGraphContract.normalize(g)));
  return {
    lineage_fingerprint: computeKaalkaHashPayload({ hashes }),
    count: graphs.length,
    bounded: true,
  };
}

export { graphFingerprint, computeRuntimeFingerprint } from "./runtimeGraph.js";
