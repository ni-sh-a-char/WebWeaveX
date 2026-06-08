/**
 * Converted from Python: core/database/semantic_index_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticIndex {
  declare _index: any;
  constructor() {
    this._index = {};
  }
  insert(key: any, value: any): any {
    var bucket: any = py.setdefault(this._index, key, []);
    py.listAppend(bucket, value);
  }
  lookup(key: any): any {
    return [...py.iter(py.get(this._index, key, []))];
  }
}
