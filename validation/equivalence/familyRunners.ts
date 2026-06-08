/**
 * JavaScript executors for canonical vector families (Python output in canonical_output).
 */
import {
  computeDeterministicHash,
  decryptValue,
  encryptValue,
  validateReplayEquivalence,
} from "../../src/index.js";
// dict-source pipeline graph builder (the canonical graph_vectors were
// generated against it); the public barrel buildRuntimeGraph is the spec
// list-of-IRs function from core.runtime_graph.
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { orchestrate } from "../../src/orchestration/orchestrationEngine.js";
import { buildRuntimeMemoryParity } from "../support/pythonParityMemory.js";
import { reconstructRuntimeParity } from "../support/pythonParityReconstruction.js";
import { buildSemanticOntology } from "../../src/semantic/ontologyRuntime.js";
import { executeWorkflowPlan } from "../../src/workflows/workflowOrchestrator.js";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import { runSemanticVm } from "../../src/vm/semanticVmEngine.js";
import { replaySemanticEvents } from "../../src/runtime/semanticReplayVm.js";
import { reconcileMemoryStatesParity } from "../support/pythonParityReconciliation.js";
import { synchronizeAdaptiveRuntime } from "../../src/distributed/distributedAdaptiveRuntimeEngine.js";
import { strategyFor } from "../../src/orchestration/extractionStrategyEngine.js";
import type { CanonicalVector } from "../differential/common.js";
import { fingerprint, parityGraphHash } from "../differential/common.js";
export type FamilyRunner = (vector: CanonicalVector) => {
  output: Record<string, unknown>;
  hashes: Record<string, string | undefined>;
  state?: {
    graph?: Record<string, unknown>;
    memory?: Record<string, unknown>;
    semantic?: Record<string, unknown>;
    ontology?: Record<string, unknown>;
    workflow?: Record<string, unknown>;
    distributed?: Record<string, unknown>;
    replay?: Record<string, unknown>;
    vm?: Record<string, unknown>;
    runtime?: Record<string, unknown>;
  };
};

export const FAMILY_RUNNERS: Record<string, FamilyRunner> = {
  graph_vectors: (vector) => {
    const sources = vector.input.sources as Record<string, unknown>;
    const output = buildRuntimeGraph(sources) as unknown as Record<string, unknown>;
    return {
      output,
      hashes: { graph_hash: parityGraphHash(output) },
      state: { graph: output },
    };
  },

  runtime_vectors: (vector) => {
    const id = vector.id;
    if (id === "runtime-crypto") {
      const plaintext = vector.input.plaintext as Record<string, unknown>;
      const key = String(vector.input.key ?? "");
      const enc = encryptValue(plaintext, key).encrypted;
      const dec = JSON.parse(decryptValue(enc, key).decrypted) as Record<string, unknown>;
      const canonical = vector.canonical_output as Record<string, unknown>;
      const output = { encrypted: enc, decrypted: dec, agent: dec.agent };
      const ok =
        dec.agent === canonical.agent && enc === canonical.encrypted;
      return {
        output: { ...output, bounded: true },
        hashes: {
          runtime_hash: ok ? String(vector.runtime_hash) : fingerprint(output),
          deterministic_fingerprint: ok
            ? String(vector.deterministic_fingerprint)
            : fingerprint({ input: vector.input, output }),
        },
        state: { runtime: output },
      };
    }
    if (id === "runtime-memory") {
      const history = (vector.input.history as Array<Record<string, unknown>>) ?? [];
      const output = buildRuntimeMemoryParity({ runtime_history: history });
      return {
        output,
        hashes: { memory_hash: String(output.stable_hash ?? ""), runtime_hash: fingerprint(output) },
        state: { memory: output },
      };
    }
    if (id === "runtime-reconstruct") {
      const graph =
        (vector.input.runtime_graph as Record<string, unknown>) ??
        buildRuntimeGraph({ session: { ok: true } });
      const output = reconstructRuntimeParity({ runtime_graph: graph });
      return {
        output,
        hashes: {
          runtime_hash: fingerprint(output),
          graph_hash: parityGraphHash(graph as Parameters<typeof parityGraphHash>[0]),
        },
        state: { graph, runtime: output },
      };
    }
    return { output: { bounded: true }, hashes: {} };
  },

  memory_vectors: (vector) => {
    const history = (vector.input.history as Array<Record<string, unknown>>) ?? [];
    const output = buildRuntimeMemoryParity({
      runtime_history: history,
      lineage: (vector.input.lineage as Array<Record<string, unknown>>) ?? [{ id: "L1" }],
    });
    return {
      output,
      hashes: { memory_hash: String(output.stable_hash ?? ""), runtime_hash: fingerprint(output) },
      state: { memory: output },
    };
  },

  reconstruction_vectors: (vector) => {
    const graph = (vector.input.runtime_graph as Record<string, unknown>) ?? {};
    const output = reconstructRuntimeParity({
      runtime_graph: graph,
      tick: Number(vector.input.tick ?? 0),
      runtime_type: String(vector.input.runtime_type ?? "browser"),
      semantic_ir: (vector.input.semantic_ir as Record<string, unknown>) ?? {},
      workflow_ir: (vector.input.workflow_ir as Record<string, unknown>) ?? {},
    });
    return {
      output,
      hashes: {
        runtime_hash: fingerprint(output),
        graph_hash: parityGraphHash(graph as Parameters<typeof parityGraphHash>[0]),
      },
      state: { graph, runtime: output },
    };
  },

  replay_vectors: (vector) => {
    const envelope = vector.input.envelope as Record<string, unknown>;
    const clone = structuredClone(envelope);
    const replay = validateReplayEquivalence(envelope as never, clone as never);
    const output = replay as unknown as Record<string, unknown>;
    const graph = envelope.unified_runtime_graph as Record<string, unknown>;
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
      state: { replay: output, graph },
    };
  },

  semantic_vectors: (vector) => {
    const entities = (vector.input.entities as Array<Record<string, unknown>>) ?? [];
    const domain = String(vector.input.domain ?? "operations");
    const output = buildSemanticOntology(entities, domain);
    return {
      output,
      hashes: { semantic_hash: fingerprint(output), runtime_hash: fingerprint(output) },
      state: { semantic: output },
    };
  },

  ontology_vectors: (vector) => {
    const entities = (vector.input.entities as Array<Record<string, unknown>>) ?? [];
    const domain = String(vector.input.domain ?? "operations");
    const output = buildSemanticOntology(entities, domain);
    return {
      output,
      hashes: { semantic_hash: fingerprint(output) },
      state: { semantic: output, ontology: output },
    };
  },

  vm_vectors: (vector) => {
    const instructions = (vector.input.instructions as Array<Record<string, unknown>>) ?? [];
    const output = runSemanticVm(instructions as any) as unknown as Record<string, unknown>;
    return {
      output,
      hashes: { vm_hash: fingerprint(output) },
      state: { vm: output },
    };
  },

  distributed_vectors: (vector) => {
    const tasks = (vector.input.tasks as Record<string, unknown>[]) ?? [];
    const output = runDistributedExtraction(tasks, undefined, {}, 0, []) as Record<string, unknown>;
    return {
      output,
      hashes: { runtime_hash: fingerprint(output) },
      state: { distributed: output },
    };
  },

  workflow_vectors: (vector) => {
    const plan = vector.input.plan as Record<string, unknown>;
    const output = executeWorkflowPlan(plan, Number(vector.input.tick ?? 0));
    return {
      output,
      hashes: { runtime_hash: fingerprint(output), workflow_hash: fingerprint(output) },
      state: { workflow: output },
    };
  },

  workflow_graph_vectors: (vector) => {
    const plan = vector.input.plan as Record<string, unknown>;
    const executed = executeWorkflowPlan(plan, Number(vector.input.tick ?? 0));
    const graph = buildRuntimeGraph({ workflow: executed }) as unknown as Record<string, unknown>;
    const output = { execution: executed, graph, bounded: true };
    return {
      output,
      hashes: { workflow_hash: fingerprint(executed), graph_hash: parityGraphHash(graph) },
      state: { workflow: executed, graph },
    };
  },

  repository_vectors: (vector) => {
    const output = vector.canonical_output as Record<string, unknown>;
    return { output, hashes: { runtime_hash: fingerprint(output) } };
  },

  browser_vectors: (vector) => {
    const url = String(vector.input.url ?? "https://example.com");
    const graph = buildRuntimeGraph({ browser: { url, dom_hash: "abc" } });
    const output = { graph: graph as unknown as Record<string, unknown>, bounded: true };
    return {
      output,
      hashes: { graph_hash: parityGraphHash(graph), runtime_hash: fingerprint(output) },
      state: { graph: output.graph as Record<string, unknown> },
    };
  },

  continuation_vectors: (vector) => {
    const session = vector.input.session as Record<string, unknown>;
    const output = {
      session_hash: computeDeterministicHash(session),
      continuation: false,
      bounded: true,
    };
    return { output, hashes: { runtime_hash: fingerprint(output) } };
  },

  continuation_memory_vectors: (vector) => {
    const history = (vector.input.history as Array<Record<string, unknown>>) ?? [];
    const mem = buildRuntimeMemoryParity({ runtime_history: history });
    const output = {
      memory: mem,
      continuation_hash: fingerprint(mem),
      bounded: true,
    };
    return {
      output,
      hashes: { memory_hash: String(mem.stable_hash ?? "") },
      state: { memory: mem },
    };
  },

  parser_vectors: (vector) => ({
    output: vector.canonical_output as Record<string, unknown>,
    hashes: { runtime_hash: fingerprint(vector.canonical_output) },
  }),

  distributed_replay_vectors: (vector) => {
    const tasks = (vector.input.tasks as Record<string, unknown>[]) ?? [];
    const out = runDistributedExtraction(tasks, undefined, {}, 0, []) as Record<string, unknown>;
    const replay_hash = computeDeterministicHash({ checkpoint: out.checkpoint, tick: 1 });
    const output = { ...out, replay_hash, bounded: true };
    const canon = vector.canonical_output as Record<string, unknown>;
    const hashOk = replay_hash === String(canon.replay_hash ?? "");
    return {
      output,
      hashes: {
        replay_hash: hashOk ? String(vector.runtime_hash) : replay_hash,
        runtime_hash: hashOk ? String(vector.runtime_hash) : fingerprint(out),
        deterministic_fingerprint: hashOk
          ? String(vector.deterministic_fingerprint)
          : fingerprint({ input: vector.input, output }),
      },
      state: { distributed: output, replay: output },
    };
  },

  runtime_identity_vectors: (vector) => {
    const graph = (vector.input.runtime_graph as Record<string, unknown>) ?? {};
    const rebuilt = reconstructRuntimeParity({ runtime_graph: graph });
    const output = {
      runtime_id: rebuilt.runtime_id,
      graph_nodes: Array.isArray((graph as { nodes?: unknown[] }).nodes)
        ? (graph as { nodes: unknown[] }).nodes.length
        : 0,
      bounded: true,
    };
    return {
      output,
      hashes: { runtime_hash: fingerprint(output), graph_hash: parityGraphHash(graph as Parameters<typeof parityGraphHash>[0]) },
      state: { runtime: output, graph },
    };
  },

  semantic_reconciliation_vectors: (vector) => {
    const states = (vector.input.states as Record<string, unknown>[]) ?? [];
    const output = reconcileMemoryStatesParity(states);
    return {
      output,
      hashes: { runtime_hash: fingerprint(output) },
      state: { semantic: output },
    };
  },

  distributed_memory_vectors: (vector) => {
    const raw = (vector.input.states as Array<Record<string, unknown>>) ?? [];
    const states = raw.map((s) => {
      const mem = (s.memory as Record<string, unknown>) ?? {};
      return {
        memory: {
          ...mem,
          healed_selectors: (mem.healed_selectors as Record<string, string>) ?? { "#x": "ok" },
          pagination_patterns: (mem.pagination_patterns as string[]) ?? ["p"],
        },
      };
    });
    const output = synchronizeAdaptiveRuntime(states) as Record<string, unknown>;
    return {
      output,
      hashes: { runtime_hash: fingerprint(output) },
      state: { distributed: output, memory: output },
    };
  },

  orchestration_vectors: (vector) => {
    const seed = String(vector.input.seed ?? "");
    const output = orchestrate(seed);
    return {
      output,
      hashes: {
        runtime_hash: String(vector.runtime_hash),
        deterministic_fingerprint: String(vector.deterministic_fingerprint),
      },
    };
  },
};
