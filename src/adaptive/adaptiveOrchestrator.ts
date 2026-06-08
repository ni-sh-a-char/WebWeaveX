export function runAdaptiveExtraction(
  selector: string,
  html: string,
  domNodes: Array<Record<string, unknown>> = [],
): Record<string, unknown> {
  const healed =
    domNodes.find((n) => String(n.text ?? "").includes(selector.replace(/^#/, ""))) != null
      ? selector
      : domNodes[0]
        ? `#${String((domNodes[0]!.attrs as Record<string, unknown>)?.id ?? "root")}`
        : selector;
  const stabilized = html.replace(/\s+/g, " ").trim();
  return {
    stabilized_html: stabilized,
    healed_selector: healed,
    bounded: true,
    selector_attempts: [selector, healed],
  };
}
