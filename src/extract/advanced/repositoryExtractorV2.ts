/**
 * Converted from Python: core/extract/advanced/repository_extractor_v2.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractRepositoryV2(text: any): any {
  var src: any = py.or2(text, () => (""));
  var files: any = py.sorted(py.toSet(py.reFindall("[A-Za-z0-9_./-]+", src, "")));
  var ci: any = py.sorted(py.toSet(py.iter(files).filter((f: any) => (py.truthy(py.endswith(f, [".yml", ".yaml"])) && (py.contains(f, ".github/workflows") || py.contains(f, "gitlab-ci") || py.contains(f, "bitbucket-pipelines")))).map((f: any) => f)));
  var containers: any = py.sorted(py.toSet(py.iter(files).filter((f: any) => (py.contains(["Dockerfile", "docker-compose.yml", "docker-compose.yaml"], f) || py.truthy(py.endswith(f, "Dockerfile")))).map((f: any) => f)));
  var infra: any = py.sorted(py.toSet(py.iter(files).filter((f: any) => py.any(py.iter(["terraform", "helm", "k8s", "kubernetes"]).map((x: any) => py.contains(f, x)))).map((f: any) => f)));
  var configs: any = py.sorted(py.toSet(py.iter(files).filter((f: any) => py.truthy(py.endswith(f, [".json", ".toml", ".yaml", ".yml", ".ini", ".cfg"]))).map((f: any) => f)));
  var entrypoints: any = py.sorted(py.toSet(py.iter(files).filter((f: any) => py.truthy(py.endswith(f, ["main.py", "app.py", "index.js", "main.dart", "Main.java"]))).map((f: any) => f)));
  return {"repository_structure": py.slice(files, null, 2000), "entrypoints": entrypoints, "ci_cd_files": ci, "infra_files": infra, "container_files": containers, "config_files": configs};
}
