/**
 * Converted from Python: core/internet/intelligence/crawl_priority_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function rankCrawlPriority(urls: any): any {
  return py.sorted(py.toSet(py.or2(urls, () => ([]))), {key: ((u: any) => [py.count(u, "/"), py.len(u), u]) as (item: any) => any});
}
