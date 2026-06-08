/**
 * Converted from Python: core/world_model/semantic_context_compression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CONTEXT_KEYS: any = 256;
export function compressSemanticContext(state: any): any {
  var keys: any = py.slice(py.sorted(py.keys(state)), null, MAX_CONTEXT_KEYS);
  return {"compressed": Object.fromEntries(py.iter(keys).map((key: any) => ([key, py.at(state, key)] as [any, any]))), "compression_ratio": py.round(py.div(py.len(keys), py.max([py.len(state), 1])), 3)};
}
