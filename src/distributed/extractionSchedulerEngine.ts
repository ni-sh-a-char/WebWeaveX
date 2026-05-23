const MAX_SCHEDULED = 5000;
const DEFAULT_COOLDOWN = 5;

export function scheduleExtractionRuntime(
  tasks: Record<string, unknown>[],
  tick = 0,
): Record<string, unknown> {
  const scheduled: Record<string, unknown>[] = [];
  for (const [index, task] of tasks.slice(0, MAX_SCHEDULED).entries()) {
    const priority = Number(task.priority ?? 0);
    const retries = Number(task.retries ?? 0);
    const cooldown = Number(task.cooldown ?? DEFAULT_COOLDOWN);
    const pacing = Number(task.pacing ?? 1);
    scheduled.push({
      task_id: String(task.task_id ?? `task_${index}`),
      url: String(task.url ?? ""),
      priority,
      run_at: tick + cooldown * retries + pacing * index,
      retries,
      bounded: true,
    });
  }
  scheduled.sort(
    (a, b) =>
      Number(a.run_at ?? 0) - Number(b.run_at ?? 0) ||
      Number(b.priority ?? 0) - Number(a.priority ?? 0) ||
      String(a.task_id).localeCompare(String(b.task_id)),
  );
  return { scheduled, tick, bounded: true };
}
