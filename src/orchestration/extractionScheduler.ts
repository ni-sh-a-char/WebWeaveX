/** Mirrors core.orchestration.extraction_scheduler.schedule */
export function schedule(plan: Record<string, unknown>): Record<string, unknown> {
  const order = (plan.extraction_order as string[]) ?? [];
  return { scheduled: [...order] };
}
