/**
 * Converted from Python: core/extract/architecture_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ARCH_SECTIONS: any = ["architecture", "design", "flow", "components", "overview"];
export function extractArchitecture(text: any): any {
  var src: any = py.or2(text, () => (""));
  var lines: any = py.iter(py.splitlines(src)).filter((line: any) => py.truthy(py.strip(line))).map((line: any) => py.strip(line));
  var matched: any = py.iter(lines).filter((ln: any) => py.any(py.iter(ARCH_SECTIONS).map((s: any) => py.contains(String(ln).toLowerCase(), s)))).map((ln: any) => ln);
  var routes: any = py.sorted(py.toSet(py.reFindall("(?:GET|POST|PUT|PATCH|DELETE)\\s+(/[A-Za-z0-9_\\-/{}:]+)", src, "")));
  return {"sections": py.sorted(py.toSet(matched)), "api_routes": routes};
}
