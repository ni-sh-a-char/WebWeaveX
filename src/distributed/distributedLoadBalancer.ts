const MAX_WORKERS = 1000;

export function balanceExtractionWorkloads(
  workers: Record<string, unknown>[],
  tasks: Record<string, unknown>[],
): Record<string, unknown> {
  if (!workers.length) return { assignments: [], bounded: true };
  const active = workers
    .slice(0, MAX_WORKERS)
    .sort((a, b) => String(a.worker_id).localeCompare(String(b.worker_id)));
  const assignments = tasks.map((task, index) => {
    const worker = active[index % active.length]!;
    return {
      task_id: String(task.task_id ?? `task_${index}`),
      worker_id: String(worker.worker_id ?? ""),
      partition: index % active.length,
    };
  });
  assignments.sort(
    (a, b) =>
      String(a.worker_id).localeCompare(String(b.worker_id)) ||
      String(a.task_id).localeCompare(String(b.task_id)),
  );
  return { assignments, bounded: true };
}
