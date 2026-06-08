/**
 * Converted from Python: core/repository/intelligence/repository_ast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

const ast: any = py.astModule;
export function _pyAst(src: any): any {
  var out: any = {"symbols": [], "imports": [], "classes": [], "functions": []};
  try {
    var tree: any = ast.parse(src);
  } catch (_e: any) {
    return out;
  }
  var n: any;
  for (n of py.iter(ast.walk(tree))) {
    if ((true)) {
      py.extend(py.at(out, "imports"), py.iter(n.names).map((a: any) => a.name));
    } else if ((true)) {
      if (py.truthy(n.module)) {
        py.listAppend(py.at(out, "imports"), n.module);
      }
    } else if ((true)) {
      py.listAppend(py.at(out, "classes"), n.name);
      py.listAppend(py.at(out, "symbols"), n.name);
    } else if ((true)) {
      py.listAppend(py.at(out, "functions"), n.name);
      py.listAppend(py.at(out, "symbols"), n.name);
    }
  }
  var k: any;
  for (k of py.iter(out)) {
    py.setItem(out, k, py.sorted(py.toSet(py.at(out, k))));
  }
  return out;
}
export function _jsLike(src: any): any {
  var classes: any = py.sorted(py.toSet(py.reFindall("\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)", src, "")));
  var funcs: any = py.sorted(py.toSet(py.reFindall("\\bfunction\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*\\(", src, "")));
  var imports: any = py.sorted(py.toSet(py.reFindall("import\\s+.*?from\\s+['\"]([^'\"]+)['\"]", src, "")));
  var interfaces: any = py.sorted(py.toSet(py.reFindall("\\binterface\\s+([A-Za-z_][A-Za-z0-9_]*)", src, "")));
  var symbols: any = py.sorted(py.toSet(py.add(py.add(classes, funcs), interfaces)));
  return {"symbols": symbols, "imports": imports, "classes": classes, "functions": funcs, "interfaces": interfaces};
}
export function _javaKotlin(src: any): any {
  var imports: any = py.sorted(py.toSet(py.reFindall("\\bimport\\s+([A-Za-z0-9_.]+)", src, "")));
  var classes: any = py.sorted(py.toSet(py.reFindall("\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)", src, "")));
  var funcs: any = py.sorted(py.toSet(py.reFindall("\\b(?:fun|void|public|private|protected|static)\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*\\(", src, "")));
  var interfaces: any = py.sorted(py.toSet(py.reFindall("\\binterface\\s+([A-Za-z_][A-Za-z0-9_]*)", src, "")));
  var symbols: any = py.sorted(py.toSet(py.add(py.add(classes, funcs), interfaces)));
  return {"symbols": symbols, "imports": imports, "classes": classes, "functions": funcs, "interfaces": interfaces};
}
export function extractRepositoryAst(text: any): any {
  var src: any = py.or2(text, () => (""));
  var py_: any = _pyAst(src);
  var js: any = _jsLike(src);
  var jv: any = _javaKotlin(src);
  var languages: any[] = [];
  if ((py.truthy(py.at(py_, "imports")) || py.contains(src, "def "))) {
    py.listAppend(languages, "python");
  }
  if ((py.truthy(py.at(js, "imports")) || py.contains(src, "function ") || py.contains(src, "class "))) {
    py.listAppend(languages, "javascript_typescript");
  }
  if (py.truthy(py.at(jv, "imports"))) {
    py.listAppend(languages, "java_kotlin");
  }
  return {"languages": py.sorted(py.toSet(languages)), "symbols": py.sorted(py.toSet(py.add(py.add(py.at(py_, "symbols"), py.at(js, "symbols")), py.at(jv, "symbols")))), "imports": py.sorted(py.toSet(py.add(py.add(py.at(py_, "imports"), py.at(js, "imports")), py.at(jv, "imports")))), "classes": py.sorted(py.toSet(py.add(py.add(py.at(py_, "classes"), py.at(js, "classes")), py.at(jv, "classes")))), "functions": py.sorted(py.toSet(py.add(py.add(py.at(py_, "functions"), py.at(js, "functions")), py.at(jv, "functions")))), "interfaces": py.sorted(py.toSet(py.add(py.at(js, "interfaces"), py.at(jv, "interfaces"))))};
}
