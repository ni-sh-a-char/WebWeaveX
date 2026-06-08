import { pythonCompactSerialize, pythonKaalkaHashFromJsonString, pythonSha256Hex } from "./pythonSemanticSerializer.js";

export type RuntimeMemoryParityInput = {
  runtime_history?: Array<Record<string, unknown>>;
  lineage?: Array<Record<string, unknown>>;
  semantic_relations?: Array<Record<string, unknown>>;
};

function sortHistory(history: Array<Record<string, unknown>>): Array<Record<string, unknown>> {
  return [...history].sort(
    (a, b) => Number(a.tick ?? a.step ?? 0) - Number(b.tick ?? b.step ?? 0),
  );
}

function sortLineage(lineage: Array<Record<string, unknown>>): Array<Record<string, unknown>> {
  return [...lineage].sort((a, b) => String(a.id ?? "").localeCompare(String(b.id ?? "")));
}

function sortRelations(relations: Array<Record<string, unknown>>): Array<Record<string, unknown>> {
  return [...relations].sort(
    (a, b) =>
      String(a.from ?? "").localeCompare(String(b.from ?? "")) ||
      String(a.to ?? "").localeCompare(String(b.to ?? "")),
  );
}

/** Mirrors core.memory.runtime_memory_engine.build_runtime_memory */
export function buildRuntimeMemoryParity(input: RuntimeMemoryParityInput = {}): Record<string, unknown> {
  const runtime_history = sortHistory(input.runtime_history ?? []);
  const lineage = sortLineage(input.lineage ?? []);
  const semantic_relations = sortRelations(input.semantic_relations ?? []);

  const payload = [
    ...runtime_history.map((item) => String(item.tick ?? item.step ?? "")),
    ...lineage.map((item) => String(item.id ?? "")),
  ].join("|");
  const memory_id = pythonSha256Hex(payload, 32);

  const result: Record<string, unknown> = {
    memory_id,
    runtime_history,
    workflow_history: runtime_history.filter((item) => item.kind === "workflow"),
    synchronization_history: runtime_history.filter((item) => item.kind === "sync"),
    evolution_history: runtime_history.filter((item) => item.kind === "evolution"),
    lineage,
    semantic_relations,
    bounded: true,
  };

  const canonical = {
    memory_id: result.memory_id,
    runtime_history: result.runtime_history,
    lineage: result.lineage,
    semantic_relations: result.semantic_relations,
  };
  result.stable_hash = pythonKaalkaHashFromJsonString(pythonCompactSerialize(canonical));
  return result;
}

/** Mirrors core.memory.stable_memory_hash.stable_memory_hash */
export function stableMemoryHashParity(memory: Record<string, unknown>): string {
  const canonical = {
    memory_id: memory.memory_id ?? "",
    runtime_history: memory.runtime_history ?? [],
    lineage: memory.lineage ?? [],
    semantic_relations: memory.semantic_relations ?? [],
  };
  return pythonKaalkaHashFromJsonString(pythonCompactSerialize(canonical));
}
