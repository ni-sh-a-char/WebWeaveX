/**
 * Converted from Python: core/extract/repository_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractRepositoryData(text: any, source_url: any = ""): any {
  var src: any = py.or2(text, () => (""));
  var tree_lines: any = py.iter(py.splitlines(src)).filter((ln: any) => (py.contains(ln, "/") || py.contains(ln, "."))).map((ln: any) => py.strip(ln));
  var readme_sections: any = py.sorted(py.toSet(py.reFindall("^#{1,6}\\s+(.+)$", src, "m")));
  return {"repository": {"source": source_url, "structure_hints": py.slice(py.sorted(py.toSet(tree_lines)), null, 200)}, "readme": {"sections": readme_sections}};
}
