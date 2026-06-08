/**
 * Converted from Python: core/runtime/semantic_lock_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
// from threading import ... (unmapped)

var LOCKS: Record<string, any> = {};
export function acquireSemanticLock(key: any): any {
  if (!py.contains(LOCKS, key)) {
    py.setItem(LOCKS, key, py.lock());
  }
  return py.at(LOCKS, key).acquire(false);
}
export function releaseSemanticLock(key: any): any {
  if (py.contains(LOCKS, key)) {
    try {
      py.at(LOCKS, key).release();
    } catch (_e: any) {
    }
  }
}
