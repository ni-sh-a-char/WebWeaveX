const MAX_QUEUE_SIZE = 10000;

export function enqueueExtraction(
  queue: Record<string, unknown>[],
  task: Record<string, unknown>,
): { queue: Record<string, unknown>[]; enqueued: string; bounded: boolean } {
  let bounded = queue.slice(0, MAX_QUEUE_SIZE);
  const taskId = String(task.task_id ?? `task_${bounded.length}`);
  const entry = {
    task_id: taskId,
    url: String(task.url ?? ""),
    priority: Number(task.priority ?? 0),
    order: bounded.length,
    bounded: true,
  };
  bounded.push(entry);
  bounded = bounded
    .sort(
      (a, b) =>
        Number(b.priority ?? 0) - Number(a.priority ?? 0) ||
        Number(a.order ?? 0) - Number(b.order ?? 0) ||
        String(a.task_id).localeCompare(String(b.task_id)),
    )
    .slice(0, MAX_QUEUE_SIZE);
  return { queue: bounded, enqueued: taskId, bounded: true };
}

export function dequeueExtraction(queue: Record<string, unknown>[]): {
  task: Record<string, unknown> | null;
  queue: Record<string, unknown>[];
  bounded: boolean;
} {
  const bounded = [...queue].sort(
    (a, b) =>
      Number(b.priority ?? 0) - Number(a.priority ?? 0) ||
      Number(a.order ?? 0) - Number(b.order ?? 0) ||
      String(a.task_id).localeCompare(String(b.task_id)),
  );
  if (!bounded.length) return { task: null, queue: [], bounded: true };
  return { task: bounded[0]!, queue: bounded.slice(1), bounded: true };
}
