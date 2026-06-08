/**
 * Converted from Python: core/repository/semantic/semantic_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectSemanticRuntime(dependencies: any, build_files: any, configs: any): any {
  var deps: any = py.toSet(py.iter(py.or2(dependencies, () => ([]))).map((d: any) => String(d).toLowerCase()));
  var files: any = py.toSet(py.iter(py.or2(build_files, () => ([]))).map((f: any) => String(f).toLowerCase()));
  var cfgs: any = py.toSet(py.iter(py.or2(configs, () => ([]))).map((c: any) => String(c).toLowerCase()));
  var runtimes: Set<any> = new Set();
  if ((py.truthy(py.bitand(new Set(["django", "flask", "fastapi", "uvicorn"]), deps)) || py.contains(files, "requirements.txt"))) {
    py.setAdd(runtimes, "python");
  }
  if ((py.truthy(py.bitand(new Set(["react", "next", "express", "nestjs"]), deps)) || py.contains(files, "package.json"))) {
    py.setAdd(runtimes, "node");
  }
  if ((py.contains(files, "pom.xml") || py.contains(files, "build.gradle"))) {
    py.setAdd(runtimes, "jvm");
  }
  if (py.contains(files, "pubspec.yaml")) {
    py.setAdd(runtimes, "dart");
  }
  if (py.contains(files, "cargo.toml")) {
    py.setAdd(runtimes, "rust");
  }
  if (py.contains(files, "go.mod")) {
    py.setAdd(runtimes, "go");
  }
  var orchestration: any = py.sorted(py.iter(cfgs).filter((x: any) => py.truthy(py.endswith(x, [".yml", ".yaml", ".tf", "dockerfile"]))).map((x: any) => x));
  return {"runtimes": py.sorted(runtimes), "orchestration_configs": orchestration};
}
