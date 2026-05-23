export function planExtraction(seed: string): Record<string, unknown> {
  return {
    seed,
    steps: [
      { step: "ingest", order: 0 },
      { step: "extract", order: 1 },
      { step: "graph", order: 2 },
      { step: "memory", order: 3 },
    ],
    bounded: true,
  };
}
