/**
 * Production parity: core/workflows/workflow_queue_engine.py
 */

const _QUEUE: Record<string, unknown>[] = [];

export function enqueueWorkflow(workflow: Record<string, unknown>): Record<string, unknown> {
  const entry = {
    id: String(workflow.id ?? `wf:${_QUEUE.length}`),
    objective: String(workflow.objective ?? ""),
    priority: Number(workflow.priority ?? 0),
    workflow,
  };
  _QUEUE.push(entry);
  _QUEUE.sort((a, b) => {
    const pa = Number(a.priority ?? 0);
    const pb = Number(b.priority ?? 0);
    if (pa !== pb) return pa - pb;
    return String(a.id ?? "").localeCompare(String(b.id ?? ""));
  });
  return {
    enqueued: true,
    id: entry.id,
    position: _QUEUE.indexOf(entry),
    bounded: true,
  };
}

export function dequeueWorkflow(): Record<string, unknown> {
  if (_QUEUE.length === 0) {
    return { available: false, workflow: {}, bounded: true };
  }
  const entry = _QUEUE.shift()!;
  return { available: true, workflow: entry, bounded: true };
}

export function peekWorkflowQueue(): Record<string, unknown>[] {
  return [..._QUEUE];
}
