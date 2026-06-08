/**
 * Converted from Python: core/distributed/incremental_recrawl_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function shouldRecrawl(changed: any): any {
  return py.truthy(changed);
}
