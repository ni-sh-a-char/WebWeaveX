import stringify from "fast-json-stable-stringify";
import { RuntimeGraphContract } from "../contracts/graphContracts.js";
import { computeKaalkaHash } from "../crypto/kaalkaHash.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function computeGlobalRuntimeFingerprint(
  extraction: ExtractionEnvelope | Record<string, unknown> = {},
  graph?: RuntimeGraph,
  memory?: Record<string, unknown>,
  sync?: Record<string, unknown>,
  reconstruction?: Record<string, unknown>,
  kaalkaSeal = "",
): string {
  const normalizedGraph = RuntimeGraphContract.normalize(
    graph ?? (extraction.unified_runtime_graph as RuntimeGraph) ?? { nodes: [], edges: [] },
  );
  const runtime = (extraction.runtime ?? {}) as Record<string, unknown>;
  const domStab = (runtime.dom_stabilization ?? {}) as Record<string, unknown>;
  const spaStab = (runtime.spa_stabilization ?? {}) as Record<string, unknown>;
  const domHash = String(domStab.stabilized_hash ?? spaStab.stable_dom_hash ?? "");
  const browserIr = (extraction.browser_ir ?? {}) as Record<string, unknown>;
  const identity = String(browserIr.runtime_identity ?? "");

  const memoryBlock: Record<string, unknown> = {};
  if (memory) {
    const mem = (memory.memory ?? memory) as Record<string, unknown>;
    memoryBlock.stable_hash = memory.stable_hash ?? mem.stable_hash ?? "";
    memoryBlock.history_len = Array.isArray(mem.runtime_history) ? mem.runtime_history.length : 0;
  }

  const canonical = {
    dom_hash: domHash,
    runtime_identity: identity,
    graph_nodes: normalizedGraph.nodes.map((n) => n.id),
    graph_edges: normalizedGraph.edges.map((e) => [
      e.source ?? e.from,
      e.target ?? e.to,
      e.type,
    ]),
    memory: memoryBlock,
    sync_converged: (sync?.convergence as Record<string, unknown> | undefined)?.converged,
    reconstruction_id: (reconstruction?.runtime as Record<string, unknown> | undefined)?.runtime_id,
    kaalka_seal: kaalkaSeal,
    pipeline_hash: extraction.pipeline_hash ?? "",
  };
  return computeKaalkaHash(stringify(canonical));
}
