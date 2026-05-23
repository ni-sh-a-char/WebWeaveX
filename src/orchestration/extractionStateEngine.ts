export function initialState(seed: string): Record<string, unknown> {
  return { seed, tick: 0, status: "initialized", bounded: true };
}
