import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";
import { validateReplayEquivalence } from "./replayEquivalence.js";
import { validateGraphReplayEquivalence } from "./replayGraph.js";
import { validateMemoryReplayEquivalence } from "./replayMemory.js";
import { validateFingerprintReplayEquivalence } from "./replayFingerprint.js";

export function replayRuntimeState(extraction: ExtractionEnvelope): ExtractionEnvelope {
  return JSON.parse(JSON.stringify(extraction)) as ExtractionEnvelope;
}

export function validateFullRuntimeReplay(
  original: ExtractionEnvelope,
  replayed: ExtractionEnvelope,
): {
  equivalent: boolean;
  replay: ReturnType<typeof validateReplayEquivalence>;
  graph: ReturnType<typeof validateGraphReplayEquivalence>;
  memory: ReturnType<typeof validateMemoryReplayEquivalence> | null;
  fingerprint: ReturnType<typeof validateFingerprintReplayEquivalence>;
  bounded: boolean;
} {
  const graph = (original.unified_runtime_graph ?? { nodes: [], edges: [] }) as RuntimeGraph;
  const replayGraph = (replayed.unified_runtime_graph ?? replayed.graph ?? graph) as RuntimeGraph;
  const mem = (original as Record<string, unknown>).runtime_memory as Record<string, unknown> | undefined;
  const replayMem = (replayed as Record<string, unknown>).runtime_memory as
    | Record<string, unknown>
    | undefined;

  const replay = validateReplayEquivalence(original, replayed);
  const graphResult = validateGraphReplayEquivalence(graph, replayGraph);
  const memory =
    mem && replayMem ? validateMemoryReplayEquivalence(mem, replayMem) : null;
  const fingerprint = validateFingerprintReplayEquivalence(original, replayed, graph, mem);

  const equivalent =
    replay.equivalent &&
    graphResult.equivalent &&
    fingerprint.equivalent &&
    (memory === null || memory.equivalent);

  return { equivalent, replay, graph: graphResult, memory, fingerprint, bounded: true };
}
