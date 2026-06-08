/**
 * Converted from Python: core/causal_intelligence/semantic_runtime_wave_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_WAVES: any = 10000;
export function propagateRuntimeWaves(propagation_paths: any): any {
  var waves: any[] = [];
  var idx: any;
  var path: any;
  for ([idx, path] of py.enumerate(py.slice(propagation_paths, null, MAX_WAVES))) {
    py.listAppend(waves, {"wave": idx, "source": py.get(path, "source"), "target": py.get(path, "target")});
  }
  return {"waves": waves, "wave_count": py.len(waves), "bounded": true};
}
