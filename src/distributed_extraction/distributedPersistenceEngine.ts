/**
 * Converted from Python: core/distributed_extraction/distributed_persistence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { loadDistributedCheckpoint, saveDistributedCheckpoint } from "./distributedCheckpointEngine.js";

export function persistDistributedState(path: any, state: any, key: any): any {
  return saveDistributedCheckpoint(path, state, key);
}
export function restoreDistributedState(path: any, key: any): any {
  return loadDistributedCheckpoint(path, key);
}
export { loadDistributedCheckpoint, saveDistributedCheckpoint };
