import { planExtraction } from "./extractionPlanner.js";
import { schedule } from "./extractionScheduler.js";
import { initialState } from "./extractionStateEngine.js";
import { strategyFor } from "./extractionStrategyEngine.js";

export function orchestrate(seed: string): Record<string, unknown> {
  const plan = planExtraction(seed);
  return {
    plan,
    schedule: schedule(plan),
    state: initialState(seed),
    strategy: strategyFor(seed),
    bounded: true,
  };
}
