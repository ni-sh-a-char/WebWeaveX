/**
 * Converted from Python: core/internet/source_clustering_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function clusterSources(urls: any): any {
  var clusters: Record<string, any> = {};
  var url: any;
  for (url of py.iter(py.sorted(py.toSet(py.or2(urls, () => ([])))))) {
    var host: any = py.or2(String(py.urlparse(url).netloc).toLowerCase(), () => ("unknown"));
    py.listAppend(py.setdefault(clusters, host, []), url);
  }
  return {"clusters": py.iter(py.sorted(py.items(clusters))).map(([h, u]: any) => ({"host": h, "urls": py.sorted(u)})), "cluster_count": py.len(clusters)};
}
