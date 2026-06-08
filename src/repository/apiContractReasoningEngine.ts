/**
 * Converted from Python: core/repository/api_contract_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reasonApiSurface } from "./apiSurfaceReasoningEngine.js";

export function reasonApiContract(spec: any): any {
  var surface: any = reasonApiSurface(spec);
  var contracts: any = py.iter(py.get(surface, "paths", [])).map((p: any) => ({"path": py.at(p, "path"), "method": py.at(p, "method"), "contract": "http", "evidence": ["openapi:paths"]}));
  return {...(surface), "contracts": contracts, "contract_count": py.len(contracts)};
}
export { reasonApiSurface };
