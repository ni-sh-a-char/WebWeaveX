/**
 * Converted from Python: core/consensus/semantic_consensus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeSemanticConsensus(votes: any): any {
  var counter: Record<string, any> = {};
  var vote: any;
  for (vote of py.iter(votes)) {
    var value: any = py.toStr(py.get(vote, "value"));
    py.setItem(counter, value, py.add(py.get(counter, value, 0), 1));
  }
  if (!py.truthy(counter)) {
    return {"consensus": null};
  }
  var ordered: any = py.sorted(py.items(counter), {key: ((item: any) => [(-py.at(item, 1)), py.at(item, 0)]) as (item: any) => any});
  return {"consensus": py.at(py.at(ordered, 0), 0), "votes": ordered};
}
