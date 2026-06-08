/**
 * Converted from Python: core/repository/infra_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _INFRA_MARKERS: any = ["docker-compose", "Dockerfile", "kubernetes", "k8s/", "deployment.yaml", "helm/", ".github/workflows", "terraform", "pulumi"];
export function detectInfraSignals(files: any): any {
  var signals: any[] = [];
  var f: any;
  for (f of py.iter(py.or2(files, () => ([])))) {
    var fl: any = String(py.replace(f, "\\", "/")).toLowerCase();
    var m: any;
    for (m of py.iter(_INFRA_MARKERS)) {
      if (py.contains(fl, String(m).toLowerCase())) {
        py.listAppend(signals, {"file": f, "signal": m});
        break;
      }
    }
  }
  return {"signals": signals, "evidence": py.iter(signals).map((s: any) => `infra:${py.toStr(py.at(s, "signal"))}`), "deterministic_inputs": [`signals=${py.toStr(py.len(signals))}`]};
}
