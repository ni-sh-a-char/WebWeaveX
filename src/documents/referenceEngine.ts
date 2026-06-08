/**
 * Converted from Python: core/documents/reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractReferences(text: any): any {
  var src: any = py.or2(text, () => (""));
  var external: any = py.sorted(py.toSet(py.reFindall("https?://[^\\s\\)\\]'\"\"]+", src, "")));
  var internal: any = py.sorted(py.toSet(py.reFindall("\\[[^\\]]+\\]\\((/[^)]+)\\)", src, "")));
  var repo_refs: any = py.sorted(py.toSet(py.iter(external).filter((u: any) => py.any(py.iter(["github.com", "gitlab", "bitbucket"]).map((x: any) => py.contains(u, x)))).map((u: any) => u)));
  var pkg_refs: any = py.sorted(py.toSet(py.iter(external).filter((u: any) => py.any(py.iter(["pypi.org", "npmjs.com", "pub.dev"]).map((x: any) => py.contains(u, x)))).map((u: any) => u)));
  return {"internal_links": internal, "external_links": external, "citations": external, "repo_references": repo_refs, "package_references": pkg_refs};
}
