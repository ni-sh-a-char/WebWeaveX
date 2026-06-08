/**
 * Converted from Python: core/crawling/advanced/distributed_seed_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function splitSeeds(seeds: any, shards: any = 2): any {
  var data: any = py.sorted(py.toSet(py.or2(seeds, () => ([]))));
  var out: any = py.range(py.max([1, shards])).map((_: any) => []);
  var i: any;
  var s: any;
  for ([i, s] of py.enumerate(data)) {
    py.listAppend(py.at(out, py.mod(i, py.len(out))), s);
  }
  return out;
}
