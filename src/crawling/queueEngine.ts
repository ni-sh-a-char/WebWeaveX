/**
 * Converted from Python: core/crawling/queue_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class DeterministicQueue {
  declare _items: any;
  declare _seen: any;
  constructor() {
    this._items = [];
    this._seen = new Set();
  }
  enqueue(url: any): any {
    var u: any = py.strip(py.or2(url, () => ("")));
    if ((!py.truthy(u) || py.contains(this._seen, u))) {
      return false;
    }
    py.listAppend(this._items, u);
    py.setAdd(this._seen, u);
    return true;
  }
  dequeue(): any {
    return (py.truthy(this._items) ? py.pop(this._items, 0) : "");
  }
  peek(): any {
    return (py.truthy(this._items) ? py.at(this._items, 0) : "");
  }
  items(): any {
    return [...py.iter(this._items)];
  }
}
