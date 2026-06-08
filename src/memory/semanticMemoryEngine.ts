/**
 * Converted from Python: core/memory/semantic_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticMemory {
  declare max_entries: any;
  declare _store: any;
  declare _lineage: any;
  constructor(max_entries: any = 256) {
    this.max_entries = max_entries;
    this._store = {};
    this._lineage = {};
  }
  put(key: any, value: any, lineage: any = null): any {
    if ((py.len(this._store) >= this.max_entries)) {
      var oldest: any = py.next(py.iter(this._store));
      py.delItem(this._store, oldest);
      py.pop(this._lineage, oldest, null);
    }
    py.setItem(this._store, key, value);
    if ((lineage !== null && lineage !== undefined)) {
      py.setItem(this._lineage, key, lineage);
    }
  }
  get(key: any): any {
    return py.get(this._store, key);
  }
  snapshot(): any {
    return {"keys": py.sorted(py.keys(this._store)), "count": py.len(this._store), "bounded": (py.len(this._store) <= this.max_entries)};
  }
}
export function buildSemanticMemory(semantic: any = null, history: any = null): any {
  semantic = py.or2(semantic, () => ({}));
  history = py.or2(history, () => ([]));
  var inner: any = py.get(semantic, "semantic", semantic);
  var concepts: any[] = [];
  var entity: any;
  for (entity of py.iter(py.get(py.get(inner, "entities", {}), "entities", []))) {
    var label: any = py.toStr(py.get(entity, "label", py.get(entity, "type", "")));
    if (py.truthy(label)) {
      py.listAppend(concepts, label);
    }
  }
  return {"semantic_convergence": py.sorted(py.toSet(concepts)), "recurring_concepts": py.sorted(py.toSet(concepts)), "recurring_workflows": py.iter(history).filter((item: any) => py.eq(py.get(item, "kind"), "workflow")).map((item: any) => py.toStr(py.get(item, "objective", ""))), "recurring_structures": (((inner !== null && typeof inner === "object" && !Array.isArray(inner) && !(inner instanceof Set) && !(inner instanceof Map))) ? py.sorted(py.keys(inner)) : []), "domain": py.get(py.get(inner, "domain", {}), "domain", ""), "bounded": true};
}
