export function detectRepositoryLanguages(
  files: Array<{ extension?: string }>,
): Record<string, unknown> {
  const counts = new Map<string, number>();
  for (const f of files) {
    const ext = f.extension || ".unknown";
    counts.set(ext, (counts.get(ext) ?? 0) + 1);
  }
  const sorted = [...counts.entries()].sort((a, b) => b[1] - a[1]);
  return {
    primary: sorted[0]?.[0] ?? "",
    counts: Object.fromEntries(sorted),
    bounded: true,
  };
}
