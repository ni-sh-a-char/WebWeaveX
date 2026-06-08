/**
 * Converted from Python: core/repository/topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildTopology(text: any): any {
  var src: any = py.or2(text, () => (""));
  var paths: any = py.sorted(py.toSet(py.reFindall("[A-Za-z0-9_./-]+/[A-Za-z0-9_./-]+", src, "")));
  var modules: any = py.sorted(py.toSet(py.iter(paths).filter((p: any) => py.truthy(py.endswith(p, [".py", ".js", ".ts", ".dart", ".java", ".kt"]))).map((p: any) => p)));
  var packages: any = py.sorted(py.toSet(py.iter(paths).filter((p: any) => py.truthy(py.endswith(p, ["package.json", "pyproject.toml", "pubspec.yaml", "Cargo.toml", "pom.xml", "build.gradle"]))).map((p: any) => p)));
  var services: any = py.sorted(py.toSet(py.iter(paths).filter((p: any) => py.contains(p, "/")).map((p: any) => py.at(py.split(p, "/"), 0))));
  var entrypoints: any = py.sorted(py.toSet(py.iter(modules).filter((p: any) => py.truthy(py.endswith(p, ["main.py", "app.py", "index.js", "main.dart", "Main.java", "main.kt"]))).map((p: any) => p)));
  var boundaries: any = py.sorted(py.toSet(py.iter(modules).filter((p: any) => py.contains(p, "/")).map((p: any) => py.at(py.rsplit(p, "/", 1), 0))));
  return {"modules": modules, "services": services, "packages": packages, "entrypoints": entrypoints, "boundaries": boundaries};
}
