/**
 * Converted from Python: core/documents/reconstruction/migration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractMigrationGuides(text: any): any {
  var src: any = py.or2(text, () => (""));
  var sections: any = py.iter(py.reFinditer("^#{1,6}\\s+(.+)$", src, "m")).filter((m: any) => (py.contains(String(m.group(1)).toLowerCase(), "migration") || py.contains(String(m.group(1)).toLowerCase(), "upgrade"))).map((m: any) => py.strip(m.group(1)));
  var changes: any = py.sorted(py.toSet(py.reFindall("\\b(breaking change|deprecated|removed|renamed)\\b", src, "i")));
  return {"sections": py.sorted(py.toSet(sections)), "change_markers": changes};
}
