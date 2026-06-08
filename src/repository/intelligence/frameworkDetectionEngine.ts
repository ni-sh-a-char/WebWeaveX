/**
 * Converted from Python: core/repository/intelligence/framework_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectFrameworks(imports: any, dependencies: any): any {
  var keys: any = py.sorted(py.toSet(py.add(py.or2(imports, () => ([])), py.or2(dependencies, () => ([])))));
  var mapping: any = {"react": "React", "next": "Next.js", "vue": "Vue", "angular": "Angular", "django": "Django", "flask": "Flask", "fastapi": "FastAPI", "express": "Express", "nestjs": "NestJS", "spring": "Spring", "laravel": "Laravel", "flutter": "Flutter", "react-native": "React Native"};
  var out: any[] = [];
  var k: any;
  var v: any;
  for ([k, v] of py.items(mapping)) {
    if (py.any(py.iter(keys).map((x: any) => py.contains(String(x).toLowerCase(), k)))) {
      py.listAppend(out, v);
    }
  }
  return py.sorted(py.toSet(out));
}
