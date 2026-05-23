export function buildDistributedRuntimeGraph(
  workers: Record<string, unknown>[],
  topology: Record<string, unknown>,
): Record<string, unknown> {
  const nodes: Record<string, unknown>[] = [];
  const edges: Record<string, unknown>[] = [];
  for (const worker of workers) {
    nodes.push({
      id: String(worker.worker_id ?? ""),
      type: "worker",
      status: worker.status ?? "idle",
    });
  }
  for (const node of (topology.nodes as Record<string, unknown>[]) ?? []) {
    nodes.push({ id: String(node.id ?? ""), type: node.type ?? "runtime" });
  }
  for (let i = 0; i < workers.length - 1; i++) {
    edges.push({
      from: String(workers[i]!.worker_id ?? ""),
      to: String(workers[i + 1]!.worker_id ?? ""),
      relation: "worker_next",
    });
  }
  nodes.sort((a, b) => String(a.id).localeCompare(String(b.id)));
  return { ir: "distributed_runtime_graph", nodes, edges, bounded: true };
}
