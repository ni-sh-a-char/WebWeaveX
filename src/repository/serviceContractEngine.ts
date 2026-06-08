/**
 * Converted from Python: core/repository/service_contract_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractServiceContracts(services: any): any {
  var contracts: any[] = [];
  var svc: any;
  for (svc of py.iter(py.sorted(services, {key: ((s: any) => py.toStr(py.get(s, "name", ""))) as (item: any) => any}))) {
    py.listAppend(contracts, {"name": py.get(svc, "name"), "endpoints": py.sorted(py.or2(py.get(svc, "endpoints", []), () => ([]))), "evidence": py.sorted(py.toSet(py.or2(py.get(svc, "evidence", []), () => ([]))))});
  }
  return {"contracts": contracts, "count": py.len(contracts), "deterministic": true};
}
