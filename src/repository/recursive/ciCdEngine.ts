/**
 * Converted from Python: core/repository/recursive/ci_cd_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractCiCd(text: any): any {
  var src: any = py.or2(text, () => (""));
  var pipelines: any = py.sorted(py.toSet(py.reFindall("(?:\\.github/workflows/\\S+|gitlab-ci\\.yml|Jenkinsfile)", src, "i")));
  var deployments: any = py.sorted(py.toSet(py.reFindall("(?:kubernetes|k8s|helm|deploy)\\S*", src, "i")));
  var containers: any = py.sorted(py.toSet(py.reFindall("(?:Dockerfile|docker-compose\\.(?:yml|yaml))", src, "i")));
  var infra: any = py.sorted(py.toSet(py.reFindall("(?:terraform|\\.tf\\b)", src, "i")));
  return {"pipelines": pipelines, "deployments": deployments, "containers": containers, "infra": infra};
}
