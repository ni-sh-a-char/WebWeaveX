export function strategyFor(seed: string): Record<string, unknown> {
  return { strategy: seed.includes("http") ? "web" : "document", seed, bounded: true };
}
