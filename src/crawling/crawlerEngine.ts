/**
 * Converted from Python: core/crawling/crawler_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { CrawlBudget } from "./crawlBudgetEngine.js";
import { canonicalUrl } from "./dedupEngine.js";
import { allowUrl } from "./domainPolicyEngine.js";
import { DeterministicQueue } from "./queueEngine.js";
import { discoverLinks } from "./traversalEngine.js";
import { fetchSync } from "../fetch/httpFetcher.js";

export function crawl(seed_url: any, max_depth: any = 2, max_pages: any = 20, same_domain_only: any = false): any {
  var q: any = new DeterministicQueue();
  var seed: any = canonicalUrl(seed_url);
  q.enqueue(seed);
  var depth_map: any = {[py.toStr(seed)]: 0};
  var budget: any = new CrawlBudget(max_depth, max_pages);
  var visited: any[] = [];
  var discovered: any[] = [];
  while ((py.truthy(q.peek()) && py.lt(budget.pages, budget.max_pages))) {
    var url: any = q.dequeue();
    var depth: any = py.get(depth_map, url, 0);
    if (!py.truthy(budget.allow(depth))) {
      continue;
    }
    var fetched: any = fetchSync(url);
    var text: any = py.toStr(py.or2(py.get(fetched, "text", ""), () => ("")));
    budget.account(py.len(py.encode(text, "utf-8")));
    py.listAppend(visited, url);
    if (py.lt(depth, max_depth)) {
      var link: any;
      for (link of py.iter(discoverLinks(url, text))) {
        link = canonicalUrl(link);
        if (py.truthy(allowUrl(seed, link, same_domain_only))) {
          py.listAppend(discovered, link);
          if (py.truthy(q.enqueue(link))) {
            py.setItem(depth_map, link, py.add(depth, 1));
          }
        }
      }
    }
  }
  return {"visited": py.sorted(py.toSet(visited)), "queued": py.sorted(py.toSet(py.items(q))), "discovered": py.sorted(py.toSet(discovered)), "depth_map": Object.fromEntries(py.iter(py.sorted(py.keys(depth_map))).map((k: any) => ([k, py.at(depth_map, k)] as [any, any])))};
}
export { CrawlBudget, DeterministicQueue, allowUrl, canonicalUrl, discoverLinks, fetchSync };
