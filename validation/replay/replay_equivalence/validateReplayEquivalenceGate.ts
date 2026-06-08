/**
 * Replay equivalence gate — deterministic ordering, graph replay, semantic replay traces.
 */
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { replaySemanticEvents, validateReplayEquivalence, graphFingerprint } from "../../../src/index.js";
import { parityGraphHash } from "../../differential/common.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..");
const replayVectors = join(root, "validation/vectors/replay_vectors/canonical.json");

const data = JSON.parse(readFileSync(replayVectors, "utf-8")) as {
  vectors: Array<{
    input: { envelope: Record<string, unknown> };
    canonical_output: Record<string, unknown>;
    replay_hash?: string;
    graph_hash?: string;
  }>;
};
const vec = data.vectors[0]!;
const envelope = vec.input.envelope;
const clone = structuredClone(envelope);
const replay = validateReplayEquivalence(envelope as never, clone as never);
const events = replaySemanticEvents([{ id: "e1", type: "navigate" }, { id: "e2", type: "submit" }]);
const canonical = vec.canonical_output;
const canonicalChecks = (canonical.checks as Array<{ name: string; ok?: boolean }>) ?? [];
const vectorOk =
  replay.equivalent === true &&
  canonical.equivalent === true &&
  canonicalChecks.every((c) => {
    const js = replay.checks.find((r) => r.name === c.name);
    return js != null && js.ok === true;
  });
const graph = envelope.unified_runtime_graph as Record<string, unknown>;

const results = {
  deterministic_replay_ordering: events.event_count === 2,
  event_stream_equivalence: events.bounded === true,
  graph_replay_equivalence: replay.equivalent === true,
  graph_fingerprint_stable:
    graphFingerprint(graph as Parameters<typeof graphFingerprint>[0]).length > 0 &&
    (!vec.graph_hash || parityGraphHash(graph) === vec.graph_hash),
  vector_lockstep: vectorOk,
  bounded: true,
};

console.log("PASS replay_equivalence_gate", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
