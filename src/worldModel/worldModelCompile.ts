import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function compileWorldModel(input: Record<string, unknown>): Record<string, unknown> {
  const entities = (input.entities as unknown[]) ?? [];
  return {
    world_model_id: computeDeterministicHash({ entities: entities.length, input }),
    entities,
    bounded: true,
  };
}
