export function schedule(plan: Record<string, unknown>): Record<string, unknown> {
  const steps = (plan.steps as Record<string, unknown>[]) ?? [];
  return {
    scheduled: steps.map((s, i) => ({ ...s, run_at: i, bounded: true })),
    bounded: true,
  };
}
