/**
 * Converted from Python: core/semantic/repository_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractRepositorySemantics(files: any = null, text: any = ""): any {
  files = py.or2(files, () => ([]));
  var combined: any = `${py.toStr(text)} ${py.toStr(py.join(" ", files))}`;
  var roles: any[] = [];
  if (py.truthy(py.reSearch("api|routes|controller", combined, "i"))) {
    py.listAppend(roles, "api_surface");
  }
  if (py.truthy(py.reSearch("docker|k8s|helm|terraform", combined, "i"))) {
    py.listAppend(roles, "deployment_topology");
  }
  if (py.truthy(py.reSearch("service|worker|queue", combined, "i"))) {
    py.listAppend(roles, "service_boundary");
  }
  if (py.truthy(py.reSearch("react|vue|angular|next", combined, "i"))) {
    py.listAppend(roles, "frontend_framework");
  }
  if (py.truthy(py.reSearch("django|flask|fastapi|express", combined, "i"))) {
    py.listAppend(roles, "backend_framework");
  }
  var purpose: any = "application";
  if (py.contains(String(combined).toLowerCase(), "docs")) {
    purpose = "documentation";
  } else if (py.contains(String(combined).toLowerCase(), "infra")) {
    purpose = "infrastructure";
  }
  return {"architecture_roles": py.sorted(py.toSet(roles)), "service_boundaries": py.iter(roles).filter((r: any) => py.eq(r, "service_boundary")).map((r: any) => r), "api_ownership": py.contains(roles, "api_surface"), "deployment_topology": py.contains(roles, "deployment_topology"), "framework_semantics": py.iter(roles).filter((r: any) => py.contains(r, "framework")).map((r: any) => r), "repository_purpose": purpose, "bounded": true};
}
