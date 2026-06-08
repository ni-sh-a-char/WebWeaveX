/**
 * Converted from Python: core/distributed/crawl_resume_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resume(checkpoint_text: any): any {
  return py.jsonLoads(py.or2(checkpoint_text, () => ("{}")));
}
