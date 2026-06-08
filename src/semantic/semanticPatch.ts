export function patchSemanticState(
  base: Record<string, unknown>,
  patch: Record<string, unknown>,
): Record<string, unknown> {
  return { ...base, ...patch, bounded: true };
}

export function buildSemanticPatch(
  base: Record<string, unknown>,
  patch: Record<string, unknown>,
): Record<string, unknown> {
  const added: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(patch)) {
    if (base[k] !== v) added[k] = v;
  }
  return { base, patch, added, bounded: true };
}
