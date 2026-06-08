import { pythonStyleSerialize, pythonSha256Hex } from "./pythonSemanticSerializer.js";

export type ReconstructRuntimeParityInput = {
  semantic_ir?: Record<string, unknown>;
  workflow_ir?: Record<string, unknown>;
  synchronization_ir?: Record<string, unknown>;
  execution_ir?: Record<string, unknown>;
  memory_ir?: Record<string, unknown>;
  runtime_graph?: Record<string, unknown>;
  runtime_type?: string;
  tick?: number;
};

/** Mirrors core.reconstruction.runtime_reconstruction_engine.reconstruct_runtime */
export function reconstructRuntimeParity(input: ReconstructRuntimeParityInput = {}): Record<string, unknown> {
  const runtime_graph = input.runtime_graph ?? {};
  const canonical = {
    semantic: input.semantic_ir ?? {},
    workflow: input.workflow_ir ?? {},
    sync: input.synchronization_ir ?? {},
    execution: input.execution_ir ?? {},
    memory: input.memory_ir ?? {},
    graph_nodes: Array.isArray((runtime_graph as { nodes?: unknown }).nodes)
      ? (runtime_graph as { nodes: unknown[] }).nodes.length
      : 0,
    runtime_type: input.runtime_type ?? "browser",
    tick: input.tick ?? 0,
  };
  const runtime_id = pythonSha256Hex(pythonStyleSerialize(canonical), 32);
  return {
    runtime_id,
    runtime_type: canonical.runtime_type,
    reconstructed: true,
    graph_grounded: Boolean(runtime_graph && (canonical.graph_nodes as number) > 0),
    bounded: true,
  };
}
