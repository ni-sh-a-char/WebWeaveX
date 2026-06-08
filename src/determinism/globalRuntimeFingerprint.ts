/**
 * Cross-machine stable runtime fingerprint — faithful port of
 * core/determinism/global_runtime_fingerprint.py.
 * Hand-written production module (protected).
 */
import * as py from "../runtime/pyCompat.js";
import { RuntimeGraphContract } from "../contracts/graphContracts.js";
import { computeKaalkaHash } from "../crypto/kaalkaRuntime.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function computeGlobalRuntimeFingerprint(
  extraction: Record<string, unknown> | null = null,
  graph: RuntimeGraph | Record<string, unknown> | null = null,
  memory: Record<string, unknown> | null = null,
  sync: Record<string, unknown> | null = null,
  reconstruction: Record<string, unknown> | null = null,
  kaalkaSeal = "",
): string {
  const ext = (extraction ?? {}) as Record<string, unknown>;
  const normalizedGraph = RuntimeGraphContract.normalize(
    (graph ?? (ext.unified_runtime_graph as RuntimeGraph) ?? {}) as RuntimeGraph,
  );

  const runtime = (ext.runtime ?? {}) as Record<string, unknown>;
  let domHash = "";
  if (runtime !== null && typeof runtime === "object" && !Array.isArray(runtime)) {
    const domStab = (runtime.dom_stabilization ?? {}) as Record<string, unknown>;
    const spaStab = (runtime.spa_stabilization ?? {}) as Record<string, unknown>;
    domHash = py.toStr(
      py.or2(domStab.stabilized_hash ?? "", () => spaStab.stable_dom_hash ?? ""),
    );
  }
  const browserIr = ext.browser_ir ?? {};
  const identity =
    browserIr !== null && typeof browserIr === "object" && !Array.isArray(browserIr)
      ? ((browserIr as Record<string, unknown>).runtime_identity ?? "")
      : "";

  let memoryBlock: Record<string, unknown> = {};
  if (py.truthy(memory)) {
    const mem = memory as Record<string, unknown>;
    const inner = (mem.memory ?? {}) as Record<string, unknown>;
    memoryBlock = {
      stable_hash: mem.stable_hash ?? inner.stable_hash ?? "",
      history_len: Array.isArray(inner.runtime_history) ? inner.runtime_history.length : 0,
    };
  }

  const syncObj = (sync ?? {}) as Record<string, unknown>;
  const convergence = (syncObj.convergence ?? {}) as Record<string, unknown>;
  const recObj = (reconstruction ?? {}) as Record<string, unknown>;
  const recRuntime = (recObj.runtime ?? {}) as Record<string, unknown>;

  const canonical = {
    dom_hash: domHash,
    runtime_identity: identity,
    graph_nodes: (normalizedGraph.nodes as Record<string, unknown>[]).map((n) => n.id ?? null),
    graph_edges: (normalizedGraph.edges as Record<string, unknown>[]).map((e) => [
      e.source ?? e.from ?? null,
      e.target ?? e.to ?? null,
      e.type ?? null,
    ]),
    memory: memoryBlock,
    sync_converged: convergence.converged ?? null,
    reconstruction_id: recRuntime.runtime_id ?? "",
    kaalka_seal: kaalkaSeal,
    pipeline_hash: ext.pipeline_hash ?? "",
  };
  return computeKaalkaHash(
    py.jsonDumps(canonical, { sortKeys: true, separators: [",", ":"] }),
  );
}
