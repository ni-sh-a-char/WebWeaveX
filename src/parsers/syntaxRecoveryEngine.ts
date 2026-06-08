/**
 * Converted from Python: core/parsers/syntax_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recoverSyntax(source: any, language: any): any {
  var text: any = py.or2(source, () => (""));
  if (py.eq(String(language).toLowerCase(), "python")) {
    var lines: any = py.splitlines(text);
    var repaired: any[] = [];
    var balance: any = 0;
    var ln: any;
    for (ln of py.iter(lines)) {
      py.listAppend(repaired, py.rstrip(ln));
      balance = py.add(balance, py.sub(py.count(ln, "("), py.count(ln, ")")));
    }
    while ((balance > 0)) {
      py.listAppend(repaired, ")");
      balance = py.sub(balance, 1);
    }
    return py.join("\n", repaired);
  }
  return text;
}
