/**
 * Converted from Python: core/memory/runtime_lineage_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeLineageMemory(selector: any = null, workflow: any = null, sync: any = null, evolution: any = null, extraction: any = null): any {
  var lineage: any[] = [];
  var bucket: any;
  var items: any;
  for ([bucket, items] of py.iter([["selector", py.or2(selector, () => ([]))], ["workflow", py.or2(workflow, () => ([]))], ["sync", py.or2(sync, () => ([]))], ["evolution", py.or2(evolution, () => ([]))], ["extraction", py.or2(extraction, () => ([]))]])) {
    var index: any;
    var item: any;
    for ([index, item] of py.enumerate(py.slice(items, null, 1000))) {
      py.listAppend(lineage, {"id": py.toStr(py.get(item, "id", `${py.toStr(bucket)}:${py.toStr(index)}`)), "kind": bucket, "ancestor": py.toStr(py.get(item, "ancestor", ""))});
    }
  }
  return {"lineage": py.sorted(lineage, {key: ((item: any) => [py.at(item, "kind"), py.at(item, "id")]) as (item: any) => any}), "selector_ancestry": py.iter(lineage).filter((item: any) => py.eq(py.at(item, "kind"), "selector")).map((item: any) => item), "workflow_ancestry": py.iter(lineage).filter((item: any) => py.eq(py.at(item, "kind"), "workflow")).map((item: any) => item), "sync_ancestry": py.iter(lineage).filter((item: any) => py.eq(py.at(item, "kind"), "sync")).map((item: any) => item), "evolution_ancestry": py.iter(lineage).filter((item: any) => py.eq(py.at(item, "kind"), "evolution")).map((item: any) => item), "extraction_ancestry": py.iter(lineage).filter((item: any) => py.eq(py.at(item, "kind"), "extraction")).map((item: any) => item), "bounded": true};
}
