/**
 * Converted from Python: core/repository/package_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectPackageManagers(text: any): any {
  var src: any = py.or2(text, () => (""));
  var managers: any[] = [];
  var mapping: any = {"requirements.txt": "pip", "pyproject.toml": "poetry_or_pep621", "package.json": "npm", "pubspec.yaml": "pub", "pom.xml": "maven", "build.gradle": "gradle", "Cargo.toml": "cargo"};
  var k: any;
  var v: any;
  for ([k, v] of py.items(mapping)) {
    if (py.contains(src, k)) {
      py.listAppend(managers, v);
    }
  }
  return {"package_managers": py.sorted(py.toSet(managers))};
}
