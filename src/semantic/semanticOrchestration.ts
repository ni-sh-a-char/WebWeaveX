import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function runSemanticOrchestration(
  states: Record<string, unknown>[],
  options: Record<string, unknown> = {},
): Record<string, unknown> {
  const merged = Object.assign({}, ...states, options);
  return {
    orchestration_id: computeDeterministicHash({ states, options }),
    state: merged,
    depth: states.length,
    kind: options.kind ?? "orchestration",
    bounded: true,
  };
}
