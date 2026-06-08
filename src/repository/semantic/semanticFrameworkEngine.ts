/**
 * Converted from Python: core/repository/semantic/semantic_framework_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

let _FRAMEWORK_SIGNATURES: any = {"django": new Set(["django"]), "flask": new Set(["flask"]), "fastapi": new Set(["fastapi"]), "react": new Set(["react"]), "next.js": new Set(["next"]), "nestjs": new Set(["nestjs"]), "spring": new Set(["spring-boot", "springframework"]), "flutter": new Set(["flutter"]), "express": new Set(["express"]), "kubernetes": new Set(["kubernetes", "k8s"]), "docker": new Set(["docker"]), "terraform": new Set(["terraform"])};
export function detectSemanticFrameworks(imports: any, dependencies: any, configs: any = null): any {
  var haystack: any = py.toSet(py.iter(py.add(py.add(py.or2(imports, () => ([])), py.or2(dependencies, () => ([]))), py.or2(configs, () => ([])))).map((x: any) => String(x).toLowerCase()));
  var found: any[] = [];
  var framework: any;
  var signatures: any;
  for ([framework, signatures] of py.iter(py.sorted(py.items(_FRAMEWORK_SIGNATURES)))) {
    if (py.any(py.iter(signatures).flatMap((sig: any) => py.iter(haystack).map((item: any) => py.contains(item, sig))))) {
      py.listAppend(found, framework);
    }
  }
  return py.sorted(found);
}
