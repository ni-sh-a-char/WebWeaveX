/**
 * Converted from Python: core/internet/source_ranking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function rankSources(urls: any): any {
  function score(u: any): any {
    return [(py.truthy(py.startswith(u, "https://")) ? 0 : 1), py.len(u), u];
  }
  return py.sorted(py.toSet(py.or2(urls, () => ([]))), {key: (score) as (item: any) => any});
}
