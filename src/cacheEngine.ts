/**
 * Converted from Python: core/cache_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

var _MEMORY_CACHE: Record<string, any> = {};
export let CACHE_DIR: any = "cache_store";
export function generateCacheSignature(data: any): any {
  return py.hashNew("sha256", py.encode(py.jsonDumps(data, {sortKeys: true}))).hexdigest();
}
export function _ensureCacheDir(): any {
  if (!py.truthy(py.osPathExists(CACHE_DIR))) {
    py.osMakedirs(CACHE_DIR);
  }
}
export function generateCacheKey(user_input: any): any {
  if (!(typeof user_input === "string")) {
    user_input = py.toStr(user_input);
  }
  return py.hashNew("sha256", py.encode(user_input)).hexdigest();
}
export function _getCachePath(key: any): any {
  return py.osPathJoin(CACHE_DIR, `${py.toStr(key)}.json`);
}
export function loadCache(key: any): any {
  if (py.contains(_MEMORY_CACHE, key)) {
    return py.deepcopy(py.at(_MEMORY_CACHE, key));
  }
  _ensureCacheDir();
  var path: any = _getCachePath(key);
  if (!py.truthy(py.osPathExists(path))) {
    return null;
  }
  try {
    var f: any = py.open(path, "r");
    var data: any = py.jsonLoads(f.read());
    if (!((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)))) {
      return null;
    }
    var sig: any = py.get(data, "_signature");
    if (!py.truthy(sig)) {
      return null;
    }
    var check_data: any = Object.fromEntries(py.items(data).filter(([k, v]: any) => !py.eq(k, "_signature")).map(([k, v]: any) => ([k, v] as [any, any])));
    if (!py.eq(sig, generateCacheSignature(check_data))) {
      return null;
    }
    var required_keys: any = new Set(["human_readable", "structured_data", "ui_schema", "confidence", "source", "reconstructed_project", "version"]);
    if (!py.all(py.iter(required_keys).map((k: any) => py.contains(data, k)))) {
      return null;
    }
    py.setItem(_MEMORY_CACHE, key, data);
    return data;
  } catch (_e: any) {
    return null;
  }
}
export function shouldCache(data: any): any {
  if (!((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)))) {
    return false;
  }
  var confidence: any = py.get(data, "confidence", py.F(0.0));
  if (!((typeof confidence === "number" && Number.isInteger(confidence)) || typeof confidence === "number")) {
    return false;
  }
  if ((confidence < py.F(0.5))) {
    return false;
  }
  var required_keys: any = new Set(["human_readable", "structured_data", "ui_schema", "confidence", "source", "reconstructed_project", "version"]);
  if (!py.all(py.iter(required_keys).map((k: any) => py.contains(data, k)))) {
    return false;
  }
  return true;
}
export function saveCache(key: any, data: any): any {
  if (!((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)))) {
    return;
  }
  if (!py.truthy(shouldCache(data))) {
    return;
  }
  _ensureCacheDir();
  var path: any = _getCachePath(key);
  var data_copy: any = py.deepcopy(data);
  var sig_data: any = Object.fromEntries(py.items(data_copy).filter(([k, v]: any) => !py.eq(k, "_signature")).map(([k, v]: any) => ([k, v] as [any, any])));
  py.setItem(data_copy, "_signature", generateCacheSignature(sig_data));
  var temp_path: any = py.add(path, ".tmp");
  var f: any = py.open(temp_path, "w");
  f.write(py.jsonDumps(data_copy));
  py.osReplace(temp_path, path);
  py.setItem(_MEMORY_CACHE, key, py.deepcopy(data_copy));
}
export function clearCache(key: any = null): any {
  if (py.truthy(key)) {
    if (py.contains(_MEMORY_CACHE, key)) {
      py.delItem(_MEMORY_CACHE, key);
    }
    var path: any = _getCachePath(key);
    if (py.truthy(py.osPathExists(path))) {
      py.osRemove(path);
    }
  } else {
    py.clear(_MEMORY_CACHE);
    if (py.truthy(py.osPathExists(CACHE_DIR))) {
      py.rmTree(CACHE_DIR);
    }
  }
}
export function validateCacheEngine(): any {
  var test_input: any = "test_query";
  var key: any = generateCacheKey(test_input);
  var test_data: any = {"human_readable": "test", "structured_data": {"test": true}, "ui_schema": {"type": "test"}, "confidence": py.F(0.8), "source": "test", "reconstructed_project": [], "version": "v1"};
  clearCache(key);
  saveCache(key, test_data);
  var loaded: any = loadCache(key);
  if (!py.truthy(loaded)) {
    throw py.err("RuntimeError", "Cache mismatch");
  }
  var check: any = Object.fromEntries(py.items(loaded).filter(([k, v]: any) => !py.eq(k, "_signature")).map(([k, v]: any) => ([k, v] as [any, any])));
  if (!py.eq(check, test_data)) {
    throw py.err("RuntimeError", "Cache mismatch");
  }
  clearCache(key);
  return true;
}
