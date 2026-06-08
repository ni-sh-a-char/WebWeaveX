/**
 * Converted from Python: core/memory/semantic_version_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function versionSemanticState(state: any, version: any): any {
  return {"version": version, "state": state, "deterministic": true};
}
export function listVersions(versions: any): any {
  return py.sorted(versions, {key: ((v: any) => py.toInt(py.get(v, "version", 0))) as (item: any) => any});
}
