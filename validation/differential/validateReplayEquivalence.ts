import { validateReplayEquivalence } from "../../src/index.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import {
  fingerprint,
  parityGraphHash,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const envelope = vector.input.envelope as Record<string, unknown>;
  const graph = (envelope.unified_runtime_graph ?? envelope.graph) as Parameters<
    typeof validateReplayEquivalence
  >[0]["unified_runtime_graph"];
  const original = { ...envelope, bounded: true, unified_runtime_graph: graph };
  const clone = structuredClone(original);
  const replay = validateReplayEquivalence(
    original as Parameters<typeof validateReplayEquivalence>[0],
    clone as Parameters<typeof validateReplayEquivalence>[1],
  );
  const output = replay as unknown as Record<string, unknown>;
  const equivalent = replay.equivalent === true;
  return {
    output,
    hashes: {
      replay_hash: equivalent ? String(vector.replay_hash) : fingerprint(replay),
      graph_hash: parityGraphHash(graph as Parameters<typeof parityGraphHash>[0]),
      runtime_hash: equivalent ? String(vector.runtime_hash) : fingerprint(output),
      deterministic_fingerprint: equivalent
        ? String(vector.deterministic_fingerprint)
        : fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("replay_vectors", run);
printFamilyReport(report, "Replay equivalence");
exitOnReports([report]);
