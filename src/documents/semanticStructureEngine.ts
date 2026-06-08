/**
 * Converted from Python: core/documents/semantic_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractStructuralBlocks(text: any): any {
  var src: any = py.or2(text, () => (""));
  var code_blocks: any = py.reFindall("```[\\w-]*\\n(.*?)```", src, "s");
  var tables: any = py.reFindall("^\\|.*\\|$", src, "m");
  var lists: any = py.reFindall("^\\s*(?:-|\\*|\\d+\\.)\\s+.+$", src, "m");
  var configs: any = py.reFindall("(?:package\\.json|pyproject\\.toml|requirements\\.txt|pubspec\\.yaml|Cargo\\.toml)", src, "");
  var examples: any = py.reFindall("(?:^|\\n)\\s*(?:>>>|\\$)\\s+.+", src, "");
  return {"code_blocks": py.sorted(py.iter(code_blocks).filter((c: any) => py.truthy(py.strip(c))).map((c: any) => py.strip(c))), "tables": py.sorted(py.toSet(tables)), "lists": py.sorted(py.toSet(lists)), "examples": py.sorted(py.toSet(examples)), "configs": py.sorted(py.toSet(configs))};
}
