/**
 * Converted from Python: core/repository/intelligence/language_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectLanguages(text: any): any {
  var src: any = py.or2(text, () => (""));
  var langs: any[] = [];
  if (py.truthy(py.reSearch("\bdef\\s+\\w+\\(", src, ""))) {
    py.listAppend(langs, "python");
  }
  if ((py.contains(src, "import ") && (py.contains(src, "from '") || py.contains(src, "from \"")))) {
    py.listAppend(langs, "javascript");
  }
  if (py.contains(src, "fun ")) {
    py.listAppend(langs, "kotlin");
  }
  if (py.contains(src, "public class")) {
    py.listAppend(langs, "java");
  }
  if (py.contains(src, "import 'package:")) {
    py.listAppend(langs, "dart");
  }
  return py.sorted(py.toSet(langs));
}
