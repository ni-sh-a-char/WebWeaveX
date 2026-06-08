/**
 * Converted from Python: core/crawling/advanced/adaptive_scheduler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function scoreUrl(url: any): any {
  var u: any = String(py.or2(url, () => (""))).toLowerCase();
  return py.add(py.add((py.contains(u, "docs") ? 3 : 0), (py.contains(u, "api") ? 2 : 0)), (py.contains(u, "github.com") ? 2 : 0));
}
export function schedule(urls: any): any {
  return py.sorted(py.toSet(py.or2(urls, () => ([]))), {key: ((u: any) => [(-scoreUrl(u)), u]) as (item: any) => any});
}
