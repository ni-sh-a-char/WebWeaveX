import { computeGlobalRuntimeFingerprint } from "../determinism/globalRuntimeFingerprint.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";
import { graphReplayHash } from "./replayGraph.js";

export function computeReplayFingerprint(
  envelope: ExtractionEnvelope,
  graph?: RuntimeGraph,
  memory?: Record<string, unknown>,
): string {
  return computeGlobalRuntimeFingerprint(envelope, graph, memory);
}

export function validateFingerprintReplayEquivalence(
  original: ExtractionEnvelope,
  replayed: ExtractionEnvelope,
  graph?: RuntimeGraph,
  memory?: Record<string, unknown>,
): {
  equivalent: boolean;
  global_fingerprint_match: boolean;
  graph_hash_match: boolean;
  bounded: boolean;
} {
  const g = graph ?? (original.unified_runtime_graph as RuntimeGraph);
  const rg = (replayed.unified_runtime_graph ?? replayed.graph ?? g) as RuntimeGraph;
  const origFp = computeReplayFingerprint(original, g, memory);
  const replayFp = computeReplayFingerprint(replayed, rg, memory);
  const graph_hash_match = graphReplayHash(g) === graphReplayHash(rg);
  return {
    equivalent: origFp === replayFp && graph_hash_match,
    global_fingerprint_match: origFp === replayFp,
    graph_hash_match,
    bounded: true,
  };
}
