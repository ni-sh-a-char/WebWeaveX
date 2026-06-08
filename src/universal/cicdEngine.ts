/**
 * Converted from Python: core/universal/cicd_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseCicd(text: any): any {
  var src: any = py.or2(text, () => (""));
  var providers: any[] = [];
  if (py.contains(src, ".github/workflows")) {
    py.listAppend(providers, "github_actions");
  }
  if (py.contains(src, "gitlab-ci")) {
    py.listAppend(providers, "gitlab_ci");
  }
  if (py.contains(String(src).toLowerCase(), "jenkinsfile")) {
    py.listAppend(providers, "jenkins");
  }
  var jobs: any = py.sorted(py.toSet(py.reFindall("\\bjobs?:\\s*([A-Za-z0-9_-]+)?", src, "i")));
  return {"providers": py.sorted(py.toSet(providers)), "jobs": py.iter(jobs).filter((j: any) => py.truthy(j)).map((j: any) => j)};
}
