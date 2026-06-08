/**
 * Converted from Python: core/crawling/crawl_resume_v3_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resumeCrawlV3(checkpoint: any): any {
  var payload: any = py.get(py.or2(checkpoint, () => ({})), "checkpoint", "{}");
  try {
    var obj: any = py.jsonLoads(payload);
    return (((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map))) ? obj : {});
  } catch (_e: any) {
    return {};
  }
}
