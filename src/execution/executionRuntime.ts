const ALLOWLIST = new Set(["simulate", "checkpoint", "rollback", "noop"]);

export type ExecutionAction = {
  action: string;
  payload?: Record<string, unknown>;
};

export function runExecutionRuntime(
  actions: ExecutionAction[],
): { results: unknown[]; bounded: boolean; denied: string[] } {
  const results: unknown[] = [];
  const denied: string[] = [];
  for (const step of actions) {
    if (!ALLOWLIST.has(step.action)) {
      denied.push(step.action);
      continue;
    }
    results.push({ action: step.action, status: "ok", payload: step.payload ?? {} });
  }
  return { results, bounded: true, denied };
}
