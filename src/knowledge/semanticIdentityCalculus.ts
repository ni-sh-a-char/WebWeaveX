/**
 * Converted from Python: core/knowledge/semantic_identity_calculus.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function identityHash(name: any, namespace: any = ""): any {
  var raw: any = py.encode(`${py.toStr(namespace)}:${py.toStr(name)}`, "utf-8");
  var digest: any = py.slice(py.hashNew("sha256", raw).hexdigest(), null, 16);
  return {"name": name, "namespace": namespace, "id": digest, "deterministic_inputs": [`name=${py.toStr(name)}`, `namespace=${py.toStr(namespace)}`]};
}
