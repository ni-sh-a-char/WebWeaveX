/**
 * Converted from Python: core/repository/runtime_reconciliation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { reconcileMemoryStates } from "../memory/semanticReconciliationMemory.js";

export function reconcileRuntimeStates(states: any): any {
  return reconcileMemoryStates(states);
}
export { reconcileMemoryStates };
