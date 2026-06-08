/**
 * Converted from Python: core/crawling/crawl_budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_DEPTH: any = 3;
export let MAX_PAGES: any = 100;
export let MAX_BYTES: any = 50000000;
export class CrawlBudget {
  declare pages: any;
  declare bytes_seen: any;
  declare max_depth: any;
  declare max_pages: any;
  declare max_bytes: any;
  declare max_domain_visits: any;
  declare timeout_budget: any;
  constructor(max_depth: any = MAX_DEPTH, max_pages: any = MAX_PAGES, max_bytes: any = MAX_BYTES, max_domain_visits: any = 50, timeout_budget: any = py.F(30.0), pages: any = 0, bytes_seen: any = 0) {
    this.max_depth = max_depth;
    this.max_pages = max_pages;
    this.max_bytes = max_bytes;
    this.max_domain_visits = max_domain_visits;
    this.timeout_budget = timeout_budget;
    this.pages = pages;
    this.bytes_seen = bytes_seen;
  }
  allow(depth: any, add_bytes: any = 0): any {
    return py.and2(py.le(depth, this.max_depth), () => (py.and2(py.lt(this.pages, this.max_pages), () => (py.le(py.add(this.bytes_seen, add_bytes), this.max_bytes)))));
  }
  account(size: any): any {
    this.pages = py.add(this.pages, 1);
    this.bytes_seen = py.add(this.bytes_seen, py.max([size, 0]));
  }
}
