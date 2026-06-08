/**
 * Converted from Python: core/distributed/crawl_priority_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function prioritizeCrawlFrontier(urls: any): any {
  function score(u: any): any {
    var p: any = py.urlparse(u);
    var path_depth: any = py.len(py.iter(py.split(p.path, "/")).filter((x: any) => py.truthy(x)).map((x: any) => x));
    return [p.netloc, path_depth, p.path, u];
  }
  return py.sorted(py.toSet(py.or2(urls, () => ([]))), {key: (score) as (item: any) => any});
}
