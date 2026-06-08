export function executeContinuationVm(
  state: Record<string, unknown>,
  continuation: Record<string, unknown>,
): Record<string, unknown> {
  return {
    continued: true,
    state: { ...state, ...continuation },
    bounded: true,
  };
}
