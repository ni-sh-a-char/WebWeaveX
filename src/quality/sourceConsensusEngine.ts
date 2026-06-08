/**
 * Converted from Python: core/quality/source_consensus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function sourceConsensus(sources: any): any {
  var votes: Record<string, any> = {};
  var s: any;
  for (s of py.iter(py.or2(sources, () => ([])))) {
    var k: any;
    var v: any;
    for ([k, v] of py.iter(py.sorted(py.items(py.or2(s, () => ({})))))) {
      py.setdefault(votes, [k, py.toStr(v)], 0);
      py.setItem(votes, [k, py.toStr(v)], py.add(py.at(votes, [k, py.toStr(v)]), 1));
    }
  }
  var consensus: any = py.sorted(py.items(votes), {key: ((kv: any) => [(-py.at(kv, 1)), py.at(kv, 0)]) as (item: any) => any});
  return {"consensus": py.iter(py.slice(consensus, null, 20)).map(([k, n]: any) => ({"field": py.at(k, 0), "value": py.at(k, 1), "votes": n}))};
}
