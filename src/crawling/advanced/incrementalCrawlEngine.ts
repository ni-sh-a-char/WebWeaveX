/**
 * Converted from Python: core/crawling/advanced/incremental_crawl_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function diffCrawlStates(previous: any, current: any): any {
  var p: any = py.toSet(py.get(previous, "visited", []));
  var c: any = py.toSet(py.get(current, "visited", []));
  return {"new_visited": py.sorted(py.sub(c, p)), "removed": py.sorted(py.sub(p, c))};
}
