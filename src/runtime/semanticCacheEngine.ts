/**
 * Converted from Python: core/runtime/semantic_cache_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export class SemanticCache {
  declare _cache: any;
  constructor() {
    this._cache = {};
  }
  _fingerprint(payload: any): any {
    var encoded: any = py.jsonDumps(payload, {sortKeys: true, defaultStr: true});
    return py.hashNew("sha256", py.encode(encoded, "utf-8")).hexdigest();
  }
  put(payload: any, value: any): any {
    var fp: any = this._fingerprint(payload);
    py.setItem(this._cache, fp, value);
    return fp;
  }
  get(payload: any): any {
    var fp: any = this._fingerprint(payload);
    return py.get(this._cache, fp);
  }
}
