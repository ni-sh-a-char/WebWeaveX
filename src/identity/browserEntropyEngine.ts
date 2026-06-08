/**
 * Converted from Python: core/identity/browser_entropy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";

export function computeRuntimeEntropy(identity: any, observed: any = null): any {
  var baseline: any = computeKaalkaHashPayload(normalizeBrowserFingerprint(identity));
  if (!py.truthy(observed)) {
    return {"entropy_score": py.F(0.0), "stable": true, "baseline_hash": baseline, "bounded": true};
  }
  var observed_hash: any = computeKaalkaHashPayload(normalizeBrowserFingerprint(observed));
  var drift: any = (py.eq(observed_hash, baseline) ? py.F(0.0) : py.F(1.0));
  return {"entropy_score": drift, "stable": py.eq(drift, py.F(0.0)), "baseline_hash": baseline, "observed_hash": observed_hash, "bounded": true};
}
export function normalizeBrowserFingerprint(identity: any): any {
  var normalized: Record<string, any> = {};
  var key: any;
  for (key of py.iter(py.sorted(py.keys(identity)))) {
    if (py.eq(key, "bounded")) {
      continue;
    }
    var value: any = py.at(identity, key);
    if (((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map)))) {
      py.setItem(normalized, key, Object.fromEntries(py.iter(py.sorted(py.keys(value))).map((k: any) => ([String(py.toStr(k)).toLowerCase(), py.at(value, k)] as [any, any]))));
    } else if ((Array.isArray(value))) {
      py.setItem(normalized, key, py.sorted(py.iter(value).map((item: any) => String(py.toStr(item)).toLowerCase())));
    } else {
      py.setItem(normalized, key, String(py.strip(py.toStr(value))).toLowerCase());
    }
  }
  return normalized;
}
export { computeKaalkaHashPayload };
