/**
 * Converted from Python: core/repository/repository_service_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let SERVICE_FILES: any = new Set(["docker-compose.yml", "docker-compose.yaml", "Dockerfile", "package.json", "requirements.txt", "pyproject.toml", "go.mod", "Cargo.toml"]);
export function detectRepositoryServices(files: any): any {
  var services: any[] = [];
  var file: any;
  for (file of py.iter(files)) {
    var name: any = py.path(py.at(file, "path")).name;
    if (py.contains(SERVICE_FILES, name)) {
      py.listAppend(services, {"file": py.at(file, "path"), "service_indicator": name});
    }
  }
  return {"services": py.sorted(services, {key: ((x: any) => py.at(x, "file")) as (item: any) => any}), "bounded": true};
}
