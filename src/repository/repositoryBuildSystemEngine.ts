/**
 * Converted from Python: core/repository/repository_build_system_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let BUILD_FILES: any = {"Makefile": "make", "package.json": "npm", "pyproject.toml": "python", "setup.py": "python", "Cargo.toml": "cargo", "go.mod": "go", "build.gradle": "gradle", "pom.xml": "maven"};
export function detectBuildSystems(files: any): any {
  var systems: any[] = [];
  var file: any;
  for (file of py.iter(files)) {
    var name: any = py.path(py.at(file, "path")).name;
    var system: any = py.get(BUILD_FILES, name);
    if (py.truthy(system)) {
      py.listAppend(systems, {"file": py.at(file, "path"), "system": system});
    }
  }
  return {"build_systems": py.sorted(systems, {key: ((x: any) => py.at(x, "file")) as (item: any) => any}), "bounded": true};
}
