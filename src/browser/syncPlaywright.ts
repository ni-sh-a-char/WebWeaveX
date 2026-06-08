/**
 * Synchronous Playwright facade — parity with Python's playwright.sync_api
 * for the operations WebWeaveX core uses. A real Chromium session is captured
 * once per page.goto() via a one-shot bridge subprocess; subsequent reads
 * (content/title/cookies/storage/events) replay from the captured bundle.
 * Hand-written production module (protected).
 */
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as py from "../runtime/pyCompat.js";

const HERE = dirname(fileURLToPath(import.meta.url));

interface Bundle {
  ok: boolean;
  html: string;
  title: string;
  final_url: string;
  cookies: Record<string, unknown>[];
  requests: Record<string, unknown>[];
  responses: Record<string, unknown>[];
  local_storage: Record<string, string>;
  session_storage: Record<string, string>;
  scroll: { scrollHeight: number; innerHeight: number };
  error: string;
}

class FakeElement {
  tag: py.PyTag;

  constructor(tag: py.PyTag) {
    this.tag = tag;
  }

  inner_text(): string {
    return this.tag.get_text();
  }

  text_content(): string {
    return this.tag.get_text();
  }

  get_attribute(name: string): unknown {
    return this.tag.get(name);
  }
}

function soupSelect(soup: py.PySoup, selector: string): py.PyTag | null {
  const sel = String(selector).trim();
  if (sel.startsWith("#")) {
    const id = sel.slice(1);
    for (const t of soup.find_all(null)) {
      if (String(t.get("id") ?? "") === id) return t;
    }
    return null;
  }
  if (sel.startsWith(".")) {
    const cls = sel.slice(1);
    for (const t of soup.find_all(null)) {
      const classes = t.get("class");
      if (Array.isArray(classes) && classes.includes(cls)) return t;
    }
    return null;
  }
  return soup.find(sel.split(/[\s:[]/)[0]);
}

export class FakePage {
  private context: FakeContext;
  private bundle: Bundle | null = null;
  private soupDoc: py.PySoup | null = null;
  private extraHeaders: Record<string, string> = {};
  private handlers: Record<string, ((arg: unknown) => void)[]> = {};
  url = "";

  constructor(context: FakeContext) {
    this.context = context;
  }

  on(event: string, handler: (arg: unknown) => void): void {
    (this.handlers[event] ??= []).push(handler);
  }

  set_extra_http_headers(headers: Record<string, string>): void {
    this.extraHeaders = { ...this.extraHeaders, ...headers };
  }

  bring_to_front(): void {
    /* no-op */
  }

  goto(url: string, _opts: unknown = null): Record<string, unknown> {
    const cfg = {
      url,
      user_agent: this.context.opts.user_agent,
      viewport: this.context.opts.viewport,
      locale: this.context.opts.locale,
      timezone_id: this.context.opts.timezone_id,
      headers: this.extraHeaders,
      cookies: this.context.cookieJar,
    };
    const res = spawnSync(
      process.execPath,
      [join(HERE, "playwrightBridge.mjs"), JSON.stringify(cfg)],
      { encoding: "utf-8", maxBuffer: 64 * 1024 * 1024, timeout: 90_000 },
    );
    /* v8 ignore next 3 -- defensive: bridge subprocess failed to spawn */
    if (res.error || res.status !== 0 || !res.stdout) {
      throw py.err("Error", `Page.goto: ${res.error ? res.error.message : (res.stderr || "bridge failed").trim().slice(0, 200)}`);
    }
    this.bundle = JSON.parse(res.stdout) as Bundle;
    if (!this.bundle.ok) {
      throw py.err("Error", `Page.goto: ${this.bundle.error}`);
    }
    this.url = this.bundle.final_url;
    this.soupDoc = new py.PySoup(this.bundle.html);
    this.context.lastBundle = this.bundle;
    // replay network events through registered handlers (request order first)
    for (const r of this.bundle.requests) {
      for (const h of this.handlers["request"] ?? []) {
        h({
          url: r.url,
          method: r.method,
          resource_type: r.resource_type,
        });
      }
    }
    for (const r of this.bundle.responses) {
      for (const h of this.handlers["response"] ?? []) {
        h({ url: r.url, status: r.status });
      }
    }
    return { status: 200 };
  }

  content(): string {
    return this.bundle ? this.bundle.html : "";
  }

  title(): string {
    return this.bundle ? this.bundle.title : "";
  }

  evaluate(script: unknown): unknown {
    const s = String(script);
    if (!this.bundle) return null;
    if (s.includes("localStorage")) return { ...this.bundle.local_storage };
    if (s.includes("sessionStorage")) return { ...this.bundle.session_storage };
    if (s.includes("scrollHeight") || s.includes("innerHeight")) return { ...this.bundle.scroll };
    if (s.includes("scrollTo") || s.includes("scrollBy")) return null;
    return null;
  }

  query_selector(selector: string): FakeElement | null {
    if (!this.soupDoc) return null;
    const t = soupSelect(this.soupDoc, selector);
    return t ? new FakeElement(t) : null;
  }

  query_selector_all(selector: string): FakeElement[] {
    if (!this.soupDoc) return [];
    const base = String(selector).split(/[\s:[]/)[0]!;
    return this.soupDoc.find_all(base).map((t) => new FakeElement(t));
  }

  private requireSelector(selector: string, action: string): FakeElement {
    const el = this.query_selector(selector);
    if (!el) {
      throw py.err(
        "TimeoutError",
        `Page.${action}: Timeout 30000ms exceeded.\nCall log:\n  - waiting for locator("${selector}")`,
      );
    }
    return el;
  }

  click(selector: string): void {
    this.requireSelector(selector, "click");
  }

  fill(selector: string, _value: unknown): void {
    this.requireSelector(selector, "fill");
  }

  hover(selector: string): void {
    this.requireSelector(selector, "hover");
  }

  select_option(selector: string, _value: unknown): void {
    this.requireSelector(selector, "select_option");
  }

  wait_for_selector(selector: string, _opts: unknown = null): FakeElement {
    return this.requireSelector(selector, "wait_for_selector");
  }

  close(): void {
    /* no-op */
  }
}

export class FakeContext {
  opts: Record<string, unknown>;
  cookieJar: Record<string, unknown>[] = [];
  lastBundle: Bundle | null = null;
  private pageList: FakePage[] = [];

  constructor(
    user_agent: unknown = "",
    viewport: unknown = null,
    locale: unknown = "en-US",
    timezone_id: unknown = "UTC",
  ) {
    this.opts = {
      user_agent: py.toStr(user_agent ?? ""),
      viewport: viewport ?? { width: 1280, height: 720 },
      locale: py.toStr(locale ?? "en-US"),
      timezone_id: py.toStr(timezone_id ?? "UTC"),
    };
  }

  new_page(): FakePage {
    const p = new FakePage(this);
    this.pageList.push(p);
    return p;
  }

  pages(): FakePage[] {
    return [...this.pageList];
  }

  cookies(): Record<string, unknown>[] {
    return this.lastBundle ? [...this.lastBundle.cookies] : [...this.cookieJar];
  }

  add_cookies(cookies: Record<string, unknown>[]): void {
    this.cookieJar.push(...(cookies ?? []));
  }

  close(): void {
    /* no-op */
  }
}

export class FakeBrowser {
  new_context(
    user_agent: unknown = "",
    viewport: unknown = null,
    locale: unknown = "en-US",
    timezone_id: unknown = "UTC",
  ): FakeContext {
    return new FakeContext(user_agent, viewport, locale, timezone_id);
  }

  close(): void {
    /* no-op */
  }
}

class FakeChromium {
  launch(_headless: unknown = true): FakeBrowser {
    return new FakeBrowser();
  }
}

export class FakePlaywright {
  chromium = new FakeChromium();

  stop(): void {
    /* no-op */
  }
}

class SyncPlaywrightCtx {
  start(): FakePlaywright {
    return new FakePlaywright();
  }
}

/** playwright.sync_api.sync_playwright parity. */
export function syncPlaywright(): SyncPlaywrightCtx {
  return new SyncPlaywrightCtx();
}
