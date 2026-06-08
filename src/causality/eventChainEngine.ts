/**
 * Converted from Python: core/causality/event_chain_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildEventChain(events: any): any {
  var ordered: any = py.sorted(events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any});
  var chain: any[] = [];
  var index: any;
  var event: any;
  for ([index, event] of py.enumerate(py.slice(ordered, null, 10000))) {
    py.listAppend(chain, {"id": py.toStr(py.get(event, "id", `evt:${py.toStr(index)}`)), "runtime": py.toStr(py.get(event, "runtime", "unknown")), "type": py.toStr(py.get(event, "type", "mutation")), "step": index, "depth": index});
  }
  return {"chain": chain, "length": py.len(chain), "max_depth": (py.truthy(chain) ? py.sub(py.len(chain), 1) : 0), "synchronized": py.iter(chain).filter((item: any) => (py.truthy(chain) && !py.eq(py.get(item, "runtime"), py.at(py.at(chain, 0), "runtime")))).map((item: any) => py.at(item, "id")), "bounded": true};
}
