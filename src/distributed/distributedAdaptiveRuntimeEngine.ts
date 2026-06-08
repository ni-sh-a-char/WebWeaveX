export function synchronizeAdaptiveRuntime(
  runtimes: Record<string, unknown>[] = [],
): Record<string, unknown> {
  const healed: Record<string, unknown> = {};
  const pagination: string[] = [];
  const modals: unknown[] = [];
  const schemaFields = new Set<string>();

  for (const rt of runtimes) {
    const adaptive = (rt.adaptive_runtime as Record<string, unknown>) ?? rt;
    const mem = (rt.memory as Record<string, unknown>) ?? (adaptive.memory as Record<string, unknown>) ?? adaptive;
    const selectors =
      (mem.healed_selectors as Record<string, unknown>) ??
      (adaptive.healed_selectors as Record<string, unknown>) ??
      {};
    Object.assign(healed, selectors);

    const pages =
      (mem.pagination_patterns as string[]) ?? (adaptive.pagination_patterns as string[]) ?? [];
    pagination.push(...pages);

    const solutions =
      (mem.modal_solutions as unknown[]) ?? (adaptive.modal_solutions as unknown[]) ?? [];
    modals.push(...solutions);

    const schema = (rt.schema as Record<string, unknown>) ?? (adaptive.schema as Record<string, unknown>) ?? {};
    const fields = (schema.fields as string[]) ?? [];
    for (const f of fields) schemaFields.add(String(f));
  }

  return {
    healed_selectors: healed,
    pagination_patterns: [...new Set(pagination)].sort(),
    modal_solutions: modals,
    stable_schema_fields: [...schemaFields].sort(),
    bounded: true,
  };
}
