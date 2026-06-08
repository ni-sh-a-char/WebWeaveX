/**
 * Converted from Python: core/index/semantic_index_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticIndex {
  declare _index: any;
  constructor() {
    this._index = py.defaultdict(() => []);
  }
  add(key: any, value: any): any {
    py.listAppend(py.at(this._index, key), value);
  }
  search(key: any): any {
    return [...py.iter(py.get(this._index, key, []))];
  }
}
