/**
 * Converted from Python: core/distributed/freshness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function freshnessScore(old_hash: any, new_hash: any): any {
  return (py.eq(old_hash, new_hash) ? 0 : 1);
}
