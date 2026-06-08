/**
 * Converted from Python: core/parsers/dependency_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveDependencies(source: any, path: any = ""): any {
  var src: any = py.or2(source, () => (""));
  var deps: Set<any> = new Set();
  var managers: Set<any> = new Set();
  if ((py.contains(path, "package.json") || py.contains(src, "\"dependencies\""))) {
    py.setAdd(managers, "npm");
    try {
      var start: any = py.find(src, "{");
      if ((start >= 0)) {
        var blob: any = py.jsonLoads(py.slice(src, start, py.add(py.rfind(src, "}"), 1)));
        var section: any;
        for (section of py.iter(["dependencies", "devDependencies", "peerDependencies"])) {
          var block: any = py.get(blob, section, {});
          if (((block !== null && typeof block === "object" && !Array.isArray(block) && !(block instanceof Set) && !(block instanceof Map)))) {
            py.update(deps, py.keys(block));
          }
        }
      }
    } catch (_e: any) {
    }
  }
  if ((py.truthy(py.endswith(path, "Cargo.toml")) || py.contains(src, "[dependencies]"))) {
    py.setAdd(managers, "cargo");
    py.update(deps, py.reFindall("^([A-Za-z0-9_-]+)\\s*=\\s*\"", src, "m"));
  }
  if ((py.truthy(py.endswith(path, "go.mod")) || py.contains(py.slice(src, null, 200), "module "))) {
    py.setAdd(managers, "go");
    py.update(deps, py.reFindall("^\\s*([a-zA-Z0-9./_-]+)\\s+v", src, "m"));
  }
  py.update(deps, py.reFindall("^\\s*([A-Za-z0-9_.-]+)==[A-Za-z0-9_.-]+\\s*$", src, "m"));
  py.update(deps, py.reFindall("^\\s*([A-Za-z0-9_.-]+)\\s*[><=~!]", src, "m"));
  py.update(deps, py.reFindall("^\\s*([A-Za-z0-9_.-]+)\\s*$", src, "m"));
  py.update(deps, py.reFindall("implementation\\s+[\\\"']([A-Za-z0-9_.:-]+)[\\\"']", src, ""));
  py.update(deps, py.reFindall("<artifactId>([^<]+)</artifactId>", src, ""));
  if ((py.contains(path, "requirements.txt") || py.contains(src, "pip"))) {
    py.setAdd(managers, "pip");
  }
  if (py.contains(path, "build.gradle")) {
    py.setAdd(managers, "gradle");
  }
  if (py.contains(path, "pom.xml")) {
    py.setAdd(managers, "maven");
  }
  if (py.contains(path, "pubspec.yaml")) {
    py.setAdd(managers, "pub");
  }
  return {"dependencies": py.sorted(deps), "package_managers": py.sorted(managers)};
}
