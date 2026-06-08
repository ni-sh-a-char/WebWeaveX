/**
 * Converted from Python: core/crawling/advanced/rate_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function withinRateLimit(counter: any, limit: any = 60): any {
  return py.lt(counter, limit);
}
