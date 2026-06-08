/**
 * Converted from Python: core/parsers/symbol_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

const ast: any = py.astModule;
export function resolveSymbols(source: any, language: any, ast_tree: any = null): any {
  var lang: any = String(py.or2(language, () => ("text"))).toLowerCase();
  var src: any = py.or2(source, () => (""));
  var classes: Set<any> = new Set();
  var functions: Set<any> = new Set();
  var methods: Set<any> = new Set();
  var interfaces: Set<any> = new Set();
  var traits: Set<any> = new Set();
  var imports: Set<any> = new Set();
  var exports: Set<any> = new Set();
  var decorators: Set<any> = new Set();
  if (py.eq(lang, "python")) {
    try {
      var tree: any = ast.parse(src);
      var node: any;
      for (node of py.iter(ast.walk(tree))) {
        if ((true)) {
          py.setAdd(classes, node.name);
          var dec: any;
          for (dec of py.iter(node.decorator_list)) {
            if ((true)) {
              py.setAdd(decorators, dec.id);
            }
          }
        } else if ((true || true)) {
          py.setAdd(functions, node.name);
          for (dec of py.iter(node.decorator_list)) {
            if ((true)) {
              py.setAdd(decorators, dec.id);
            }
          }
        } else if ((true)) {
          var alias: any;
          for (alias of py.iter(node.names)) {
            py.setAdd(imports, alias.name);
            if (py.truthy(alias.asname)) {
              py.setAdd(exports, alias.asname);
            }
          }
        } else if ((true)) {
          var mod: any = py.or2(node.module, () => (""));
          py.setAdd(imports, mod);
          for (alias of py.iter(node.names)) {
            var name: any = alias.name;
            if (py.eq(name, "*")) {
              py.setAdd(exports, `${py.toStr(mod)}.*`);
            } else {
              py.setAdd(exports, py.or2(alias.asname, () => (name)));
            }
          }
        }
      }
    } catch (_e: any) {
    }
  }
  if ((!py.eq(lang, "python") || !py.truthy(classes))) {
    py.update(interfaces, py.reFindall("\\binterface\\s+([A-Za-z_][A-Za-z0-9_]*)", src, ""));
    py.update(traits, py.reFindall("\\btrait\\s+([A-Za-z_][A-Za-z0-9_]*)", src, ""));
    py.update(classes, py.reFindall("\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)", src, ""));
    py.update(functions, py.reFindall("\\b(?:def|function|fun|fn)\\s+([A-Za-z_][A-Za-z0-9_]*)", src, ""));
    py.update(methods, py.reFindall("\\b(?:public|private|protected)?\\s*\\w+\\s+(\\w+)\\s*\\(", src, ""));
  }
  var symbols: any = py.bitor(py.bitor(py.bitor(py.bitor(classes, functions), methods), interfaces), traits);
  return {"classes": py.sorted(classes), "functions": py.sorted(functions), "methods": py.sorted(methods), "interfaces": py.sorted(interfaces), "traits": py.sorted(traits), "imports": py.sorted(py.iter(imports).filter((i: any) => py.truthy(i)).map((i: any) => i)), "exports": py.sorted(exports), "decorators": py.sorted(decorators), "symbols": py.sorted(symbols)};
}
