export function initialState(seed: string): Record<string, unknown> {
  return { seed, status: "initialized" };
}
