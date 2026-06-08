/**
 * Converted from Python: core/repository/infra_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSource } from "../parsers/index.js";

let _INFRA_DEPS: any = py.toSet(new Set(["docker", "kubernetes", "terraform", "helm", "ansible", "k8s", "compose"]));
export function mapInfrastructure(text: any, path: any = ""): any {
  var parsed: any = parseSource(py.or2(text, () => ("")), path);
  var deps: any = py.iter(py.get(py.get(parsed, "dependencies", {}), "dependencies", [])).map((d: any) => String(py.toStr(d)).toLowerCase());
  var imports: any = py.iter(py.get(py.get(parsed, "symbols", {}), "imports", [])).map((i: any) => String(py.toStr(i)).toLowerCase());
  var evidence: any = py.add(deps, imports);
  var infra: any = py.sorted(py.toSet(py.iter(_INFRA_DEPS).filter((k: any) => py.any(py.iter(evidence).map((e: any) => py.contains(e, k)))).map((k: any) => k)));
  if (!py.truthy(infra)) {
    var src: any = String(py.or2(text, () => (""))).toLowerCase();
    infra = py.sorted(py.toSet(py.iter(_INFRA_DEPS).filter((k: any) => py.contains(src, k)).map((k: any) => k)));
    var evidence_kind: any = "text_fallback";
  } else {
    evidence_kind = "parser_dependencies";
  }
  return {"infrastructure": infra, "evidence": evidence_kind};
}
export { parseSource };
