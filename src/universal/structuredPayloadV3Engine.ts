/**
 * Converted from Python: core/universal/structured_payload_v3_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseStructuredPayload(text: any): any {
  var src: any = py.or2(text, () => (""));
  return {"has_openapi": py.truthy(py.reSearch("openapi\\s*:\\s*3", src, "i")), "has_graphql": py.or2(py.contains(src, "type Query"), () => (py.contains(src, "schema {"))), "has_dockerfile": py.contains(src, "FROM "), "has_ci": py.any(py.iter(["github/workflows", "gitlab-ci", "Jenkinsfile"]).map((k: any) => py.contains(src, k)))};
}
