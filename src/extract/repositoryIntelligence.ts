/**
 * Converted from Python: core/extract/repository_intelligence.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractRepositoryIntelligence(text: any, source_url: any = ""): any {
  var src: any = py.or2(text, () => (""));
  var files: any = py.sorted(py.toSet(py.reFindall("[A-Za-z0-9_./-]+\\.(?:py|js|ts|tsx|md|json|yml|yaml|toml|go|rs|java|kt|php)", src, "")));
  var ext_counter: any = py.counter(py.iter(files).map((f: any) => String(py.at(py.rsplit(f, ".", 1), (-1))).toLowerCase()));
  var languages: any = Object.fromEntries(py.iter(py.sorted(py.keys(ext_counter))).map((k: any) => ([k, py.at(ext_counter, k)] as [any, any])));
  var packages: any = py.sorted(py.toSet(py.reFindall("(?:package|module|service)\\s+([A-Za-z0-9_./-]+)", src, "i")));
  var imports: any = py.sorted(py.toSet(py.reFindall("^\\s*(?:import|from)\\s+([A-Za-z0-9_.-]+)", src, "m")));
  var configs: any = py.sorted(py.toSet(py.reFindall("(?:^|\\s)(?:package\\.json|pyproject\\.toml|requirements\\.txt|Dockerfile|docker-compose\\.yml|tsconfig\\.json)", src, "i")));
  var readme_headers: any = py.sorted(py.toSet(py.reFindall("^#{1,6}\\s+(.+)$", src, "m")));
  var api_routes: any = py.sorted(py.toSet(py.reFindall("(?:GET|POST|PUT|PATCH|DELETE)\\s+(/[A-Za-z0-9_\\-/{}/:]+)", src, "")));
  return {"repository_intelligence": {"source_url": source_url, "repository_tree": py.slice(files, null, 1000), "language_distribution": languages, "package_boundaries": py.slice(packages, null, 500), "dependency_graph": {"imports": py.slice(imports, null, 2000)}, "service_module_relationships": py.sorted(py.toSet(py.iter(packages).filter((p: any) => py.truthy(p)).map((p: any) => py.at(py.split(p, "/"), 0)))), "readme_source_alignment": {"readme_sections": py.slice(readme_headers, null, 200), "code_file_count": py.len(files)}, "framework_detection": py.sorted(py.toSet(py.reFindall("(next\\.js|react|django|flask|fastapi|spring|laravel|express|nestjs)", src, "i"))), "configuration_relationships": configs, "api_route_structure": api_routes, "monorepo_package_mapping": py.sorted(py.toSet(py.reFindall("packages/[A-Za-z0-9_.-]+", src, "")))}};
}
