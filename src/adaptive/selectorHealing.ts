export function healSelector(
  selector: string,
  domNodes: Array<Record<string, unknown>> = [],
): Record<string, unknown> {
  const strategies: Array<Record<string, unknown>> = [];
  const needle = selector.replace(/^[#.]/, "");
  for (const node of domNodes) {
    const attrs = (node.attrs as Record<string, unknown>) ?? {};
    if (attrs.id) strategies.push({ kind: "id", value: `#${attrs.id}` });
    if (attrs["data-testid"]) strategies.push({ kind: "testid", value: `[data-testid="${attrs["data-testid"]}"]` });
    if (String(node.text ?? "").includes(needle)) strategies.push({ kind: "text", value: selector });
  }
  const healed = strategies[0]?.value ?? selector;
  return { selector, strategies, healed, bounded: true };
}

export function computeDomSimilarity(a: string, b: string): number {
  if (a === b) return 1;
  if (!a || !b) return 0;
  const ta = new Set(a.split(/\s+/));
  const tb = new Set(b.split(/\s+/));
  const inter = [...ta].filter((t) => tb.has(t)).length;
  return inter / Math.max(ta.size, tb.size, 1);
}
