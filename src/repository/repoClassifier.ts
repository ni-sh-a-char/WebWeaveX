/**
 * Converted from Python: core/repository/repo_classifier.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function classifyRepo(url: any): any {
  var u: any = String(py.or2(url, () => (""))).toLowerCase();
  if (py.contains(u, "github.com")) {
    var provider: any = "github";
  } else if (py.contains(u, "gitlab")) {
    provider = "gitlab";
  } else if (py.contains(u, "bitbucket")) {
    provider = "bitbucket";
  } else {
    provider = "unknown";
  }
  return {"provider": provider};
}
