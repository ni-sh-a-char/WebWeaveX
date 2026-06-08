/**
 * Converted from Python: core/repository/repository_infra_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let INFRA_FILES: any = {"Dockerfile": "docker", "docker-compose.yml": "docker-compose", "docker-compose.yaml": "docker-compose", "terraform.tf": "terraform", "main.tf": "terraform", "deployment.yaml": "kubernetes", "deployment.yml": "kubernetes", "service.yaml": "kubernetes", "k8s.yaml": "kubernetes"};
export function detectRepositoryInfra(files: any): any {
  var infra: any[] = [];
  var file: any;
  for (file of py.iter(files)) {
    var name: any = py.path(py.at(file, "path")).name;
    var provider: any = py.get(INFRA_FILES, name);
    if (py.truthy(provider)) {
      py.listAppend(infra, {"file": py.at(file, "path"), "type": provider});
    }
  }
  return {"infra": py.sorted(infra, {key: ((x: any) => py.at(x, "file")) as (item: any) => any}), "bounded": true};
}
