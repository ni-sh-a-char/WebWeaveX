/**
 * Converted from Python: core/ir/api_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reasonApiSurface } from "../repository/apiSurfaceReasoningEngine.js";
import { emptyLineage } from "./_base.js";

export let ApiIR: any = py.at(Object, [py.toStr, Object]);
export function compileApiIr(spec: any): any {
  var surface: any = reasonApiSurface(spec);
  return {"paths": py.get(surface, "paths", []), "path_count": py.get(surface, "path_count", 0), "evidence": py.get(surface, "evidence", []), "lineage": emptyLineage("api_ir"), "confidence": {"score": (py.truthy(py.get(surface, "path_count")) ? py.F(1.0) : py.F(0.0)), "deterministic": true}};
}
export { emptyLineage, reasonApiSurface };
