export function compileExecutionReality(envelope: Record<string, unknown>): Record<string, unknown> {
  const runtime = (envelope.runtime as Record<string, unknown>) ?? {};
  const graph = (envelope.unified_runtime_graph as Record<string, unknown>) ?? {};
  const nodes = (graph.nodes as unknown[]) ?? [];
  const dom = (runtime.dom_stabilization as Record<string, unknown>) ?? {};
  return {
    available: runtime.available === true || nodes.length > 0,
    stabilized_hash: dom.stabilized_hash ?? null,
    node_count: nodes.length,
    causal_chain: nodes.length > 0 ? [{ kind: "graph", count: nodes.length }] : [],
    bounded: true,
  };
}
