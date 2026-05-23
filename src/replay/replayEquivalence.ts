import stringify from "fast-json-stable-stringify";
import { RuntimeGraphContract } from "../contracts/graphContracts.js";
import { computeKaalkaHash } from "../crypto/kaalkaRuntime.js";
import { computeStableDomHash } from "../determinism/domStabilization.js";
import { computeGlobalRuntimeFingerprint } from "../determinism/globalRuntimeFingerprint.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

function graphHash(graph: RuntimeGraph): string {
  const normalized = RuntimeGraphContract.normalize(graph);
  return computeKaalkaHash(
    stringify({ nodes: normalized.nodes, edges: normalized.edges }),
  );
}

function domSnapshotHash(envelope: ExtractionEnvelope): string | null {
  const raw =
    (envelope as Record<string, unknown>).dom_snapshot ??
    (envelope as Record<string, unknown>).dom_html ??
    (envelope.browser_ir as Record<string, unknown> | undefined)?.dom_html;
  if (typeof raw !== "string" || raw.length === 0) return null;
  return computeStableDomHash(raw);
}

export function validateReplayEquivalence(
  original: ExtractionEnvelope,
  replayed: ExtractionEnvelope,
): { equivalent: boolean; checks: Array<Record<string, unknown>>; bounded: boolean } {
  const origGraph = (original.unified_runtime_graph ?? original.graph ?? {
    nodes: [],
    edges: [],
  }) as RuntimeGraph;
  const replayGraph = (replayed.unified_runtime_graph ?? replayed.graph ?? {
    nodes: [],
    edges: [],
  }) as RuntimeGraph;

  const origFp = computeGlobalRuntimeFingerprint(original, origGraph);
  const replayFp = computeGlobalRuntimeFingerprint(replayed, replayGraph);
  const origDom = domSnapshotHash(original);
  const replayDom = domSnapshotHash(replayed);

  const checks: Array<Record<string, unknown>> = [
    {
      name: "graph_hash",
      ok: graphHash(origGraph) === graphHash(replayGraph),
      original: graphHash(origGraph).slice(0, 16),
      replay: graphHash(replayGraph).slice(0, 16),
    },
    {
      name: "global_fingerprint",
      ok: origFp === replayFp,
      original: origFp.slice(0, 16),
      replay: replayFp.slice(0, 16),
    },
    {
      name: "browser_identity",
      ok:
        (original.browser_ir as Record<string, unknown> | undefined)?.runtime_identity ===
        (replayed.browser_ir as Record<string, unknown> | undefined)?.runtime_identity,
    },
  ];

  if (origDom !== null && replayDom !== null) {
    checks.push({
      name: "dom_stabilized_hash",
      ok: origDom === replayDom,
      original: origDom.slice(0, 16),
      replay: replayDom.slice(0, 16),
    });
  }

  checks.push({
    name: "semantic_fingerprint",
    ok: origFp === replayFp && graphHash(origGraph) === graphHash(replayGraph),
  });

  return {
    equivalent: checks.every((c) => c.ok),
    checks,
    bounded: true,
  };
}
