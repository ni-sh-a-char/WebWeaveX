/**
 * Converted from Python: core/repository/semantic/semantic_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticDependencies(text: any): any {
  var source: any = py.or2(text, () => (""));
  var deps: Set<any> = new Set();
  py.update(deps, py.reFindall("^\\s*([A-Za-z0-9_.-]+)==[A-Za-z0-9_.-]+\\s*$", source, "m"));
  py.update(deps, py.reFindall("\\\"([@A-Za-z0-9_.-]+)\\\"\\s*:\\s*\\\"[~^]?[0-9*]", source, ""));
  py.update(deps, py.reFindall("implementation\\s+[\\\"']([A-Za-z0-9_.:-]+)[\\\"']", source, ""));
  py.update(deps, py.reFindall("<artifactId>([^<]+)</artifactId>", source, ""));
  py.update(deps, py.reFindall("^\\s*([A-Za-z0-9_-]+)\\s*=\\s*\\\"[0-9][^\\\"]*\\\"", source, "m"));
  var managers: any[] = [];
  if ((py.contains(source, "requirements.txt") || py.contains(source, "pip"))) {
    py.listAppend(managers, "pip");
  }
  if ((py.contains(source, "package.json") || py.contains(source, "node_modules"))) {
    py.listAppend(managers, "npm");
  }
  if (py.contains(source, "build.gradle")) {
    py.listAppend(managers, "gradle");
  }
  if (py.contains(source, "pom.xml")) {
    py.listAppend(managers, "maven");
  }
  if (py.contains(source, "Cargo.toml")) {
    py.listAppend(managers, "cargo");
  }
  if (py.contains(source, "pubspec.yaml")) {
    py.listAppend(managers, "pub");
  }
  return {"dependencies": py.sorted(deps), "package_managers": py.sorted(py.toSet(managers))};
}
