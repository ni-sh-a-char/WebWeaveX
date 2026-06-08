/**
 * Converted from Python: core/crawling/intelligence/duplicate_frontier_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function dedupFrontier(urls: any): any {
  return py.sorted(py.toSet(py.or2(urls, () => ([]))));
}
