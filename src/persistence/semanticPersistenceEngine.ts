/**
 * Converted from Python: core/persistence/semantic_persistence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function persistSemanticIr(ir: any): any {
  var encoded: any = py.jsonDumps(ir, {sortKeys: true, defaultStr: true});
  var fingerprint: any = py.hashNew("sha256", py.encode(encoded, "utf-8")).hexdigest();
  return {"fingerprint": fingerprint, "bytes": py.len(encoded), "persisted": true};
}
