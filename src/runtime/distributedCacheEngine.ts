/**
 * Converted from Python: core/runtime/distributed_cache_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export class DistributedSemanticCache {
  declare cache: any;
  constructor() {
    this.cache = {};
  }
  put(payload: any): any {
    var raw: any = py.jsonDumps(payload, {sortKeys: true, defaultStr: true});
    var key: any = py.hashNew("sha256", py.encode(raw, "utf-8")).hexdigest();
    py.setItem(this.cache, key, payload);
    return key;
  }
  get(key: any): any {
    return py.get(this.cache, key, {});
  }
}
