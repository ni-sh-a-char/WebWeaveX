/** Mirrors core.orchestration.extraction_strategy_engine.strategy_for */
export function strategyFor(url: string): Record<string, unknown> {
  const u = (url || "").toLowerCase();
  if (u.includes("github.com")) return { mode: "repository" };
  if (u.includes("docs")) return { mode: "documentation" };
  return { mode: "web" };
}
