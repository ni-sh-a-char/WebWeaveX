/**
 * Converted from Python: core/crawling/advanced/retry_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function nextRetry(attempt: any, max_retries: any = 3): any {
  return (py.lt(attempt, max_retries) ? py.add(attempt, 1) : (-1));
}
