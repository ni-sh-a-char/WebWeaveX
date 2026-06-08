/**
 * Converted from Python: core/orchestration/orchestration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { planExtraction } from "./extractionPlanner.js";
import { schedule } from "./extractionScheduler.js";
import { initialState } from "./extractionStateEngine.js";
import { strategyFor } from "./extractionStrategyEngine.js";

export function orchestrate(seed: any): any {
  var plan: any = planExtraction(seed);
  return {"plan": plan, "schedule": schedule(plan), "state": initialState(seed), "strategy": strategyFor(seed)};
}
export { initialState, planExtraction, schedule, strategyFor };
