/**
 * Converted from Python: core/crawling/intelligence/semantic_priority_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function semanticPriority(url: any): any {
  var u: any = String(py.or2(url, () => (""))).toLowerCase();
  var score: any = 0;
  if (py.contains(u, "/docs")) {
    score = py.add(score, 3);
  }
  if (py.contains(u, "api")) {
    score = py.add(score, 2);
  }
  if (py.contains(u, "github.com")) {
    score = py.add(score, 2);
  }
  return {"score": score};
}
