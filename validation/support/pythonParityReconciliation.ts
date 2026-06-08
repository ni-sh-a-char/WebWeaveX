/** Mirrors core.memory.semantic_reconciliation_memory.reconcile_memory_states */
export function reconcileMemoryStatesParity(
  states: Array<Record<string, unknown>>,
): Record<string, unknown> {
  const edges: Array<Record<string, unknown>> = [];
  for (const s of states) {
    const rel = (s.relations as Array<Record<string, unknown>>) ?? (s.edges as Array<Record<string, unknown>>) ?? [];
    edges.push(...rel);
  }
  const reconciled: Array<Record<string, unknown>> = [];
  const rejected: Array<Record<string, unknown>> = [];
  for (const e of edges) {
    const ev = (e.evidence as unknown[]) ?? [];
    if (!ev.length) {
      rejected.push({ edge: e, reason: "missing_evidence" });
      continue;
    }
    reconciled.push({ ...e, lineage: { stage: "reconcile" } });
  }
  return {
    states: states.length,
    reconciliation: {
      reconciled,
      rejected,
      merge: {
        merged: true,
        evidence: [],
        source_count: 0,
        deterministic_inputs: [`sources=${reconciled.length}`],
      },
      lineage: { stage: "ontology_reconciliation", count: reconciled.length },
    },
    deterministic: true,
  };
}
