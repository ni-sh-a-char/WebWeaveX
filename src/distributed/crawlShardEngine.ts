/**
 * Converted from Python: core/distributed/crawl_shard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function shardUrls(urls: any, shards: any = 2): any {
  var data: any = py.sorted(py.toSet(py.or2(urls, () => ([]))));
  var out: any = py.range(py.max([1, shards])).map((_: any) => []);
  var i: any;
  var u: any;
  for ([i, u] of py.enumerate(data)) {
    py.listAppend(py.at(out, py.mod(i, py.len(out))), u);
  }
  return out;
}
