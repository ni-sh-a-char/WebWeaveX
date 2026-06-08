/**
 * Converted from Python: core/distributed/shard_balancer_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function balanceShardsDeterministically(urls: any, shard_count: any = 4): any {
  shard_count = py.max([1, py.toInt(shard_count)]);
  var shards: any = Object.fromEntries(py.range(shard_count).map((i: any) => ([py.toStr(i), []] as [any, any])));
  var u: any;
  for (u of py.iter(py.sorted(py.toSet(py.or2(urls, () => ([])))))) {
    var h: any = py.toInt(py.hashNew("sha256", py.encode(u, "utf-8")).hexdigest(), 16);
    var idx: any = py.toStr(py.mod(h, shard_count));
    py.listAppend(py.at(shards, idx), u);
  }
  return Object.fromEntries(py.iter(py.sorted(py.items(shards))).map(([k, v]: any) => ([k, py.sorted(v)] as [any, any])));
}
