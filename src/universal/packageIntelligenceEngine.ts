/**
 * Converted from Python: core/universal/package_intelligence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractPackageIntelligence(text: any): any {
  var source: any = py.or2(text, () => (""));
  var managers: any[] = [];
  if ((py.contains(source, "requirements.txt") || py.truthy(py.reSearch("^[A-Za-z0-9_.-]+==", source, "m")))) {
    py.listAppend(managers, "pip");
  }
  if ((py.contains(source, "package.json") || py.contains(source, "\"dependencies\""))) {
    py.listAppend(managers, "npm");
  }
  if (py.contains(source, "pubspec.yaml")) {
    py.listAppend(managers, "pub");
  }
  if (py.contains(source, "Cargo.toml")) {
    py.listAppend(managers, "cargo");
  }
  if (py.contains(source, "pom.xml")) {
    py.listAppend(managers, "maven");
  }
  return {"package_managers": py.sorted(py.toSet(managers))};
}
