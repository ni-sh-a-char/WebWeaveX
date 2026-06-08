/**
 * Converted from Python: core/distributed/crawl_resume_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resumeCrawlV2(checkpoint: any): any {
  var payload: any = py.get(py.or2(checkpoint, () => ({})), "checkpoint", "{}");
  try {
    var data: any = py.jsonLoads(payload);
  } catch (_e: any) {
    data = {};
  }
  if (!((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)))) {
    data = {};
  }
  return data;
}
