/**
 * Converted from Python: core/native/platform/linux_atspi_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function probeLinuxAtspi(): any {
  if (!py.eq(py.sysShim.platform, "linux")) {
    return {"available": false, "reason": "not_linux", "bounded": true};
  }
  var pyatspi: any = null;
  var exc: any = py.err("ImportError", "module not available");
  return {"available": false, "reason": `atspi_unavailable:${py.toStr((Array.isArray(exc) ? "list" : exc === null ? "NoneType" : typeof exc === "string" ? "str" : typeof exc === "boolean" ? "bool" : typeof exc === "number" ? (Number.isInteger(exc) ? "int" : "float") : exc instanceof Set ? "set" : exc instanceof Error ? ((exc as Error).name || "Exception") : typeof exc === "object" ? ((exc as object).constructor === Object ? "dict" : (exc as object).constructor?.name ?? "object") : typeof exc))}`, "backend": "structural_fallback", "bounded": true};
}
export function extractLinuxAtspiSnapshot(fixture: any): any {
  var probe: any = probeLinuxAtspi();
  if (py.truthy(py.get(probe, "available"))) {
    return {...(probe), "fixture": fixture, "bounded": true};
  }
  return {...(probe), "windows": py.get(fixture, "windows", []), "nodes": py.get(fixture, "nodes", []), "bounded": true};
}
