export function synchronizeAdaptiveRuntime(
  runtimes: Record<string, unknown>[] = [],
): Record<string, unknown> {
  const healed: Record<string, unknown> = {};
  for (const rt of runtimes) {
    const mem = (rt.memory as Record<string, unknown>) ?? rt;
    const selectors = (mem.healed_selectors as Record<string, unknown>) ?? {};
    Object.assign(healed, selectors);
  }
  return { memory: { healed_selectors: healed }, synchronized: true, bounded: true };
}
