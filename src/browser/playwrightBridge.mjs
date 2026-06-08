#!/usr/bin/env node
/**
 * One-shot synchronous-bridge worker: performs a real Playwright page session
 * and emits a deterministic capture bundle as JSON on stdout.
 * Input: JSON on argv[2] or stdin — { url, user_agent, viewport, locale,
 *   timezone_id, headers, cookies }
 */
import { chromium } from "playwright";

async function main() {
  const cfg = JSON.parse(process.argv[2] ?? "{}");
  const bundle = {
    ok: false,
    html: "",
    title: "",
    final_url: cfg.url ?? "",
    cookies: [],
    requests: [],
    responses: [],
    local_storage: {},
    session_storage: {},
    scroll: { scrollHeight: 0, innerHeight: 0 },
    error: "",
  };
  let browser = null;
  try {
    browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({
      userAgent: cfg.user_agent || undefined,
      viewport: cfg.viewport || { width: 1280, height: 720 },
      locale: cfg.locale || "en-US",
      timezoneId: cfg.timezone_id || "UTC",
    });
    if (Array.isArray(cfg.cookies) && cfg.cookies.length) {
      try { await ctx.addCookies(cfg.cookies); } catch { /* ignore */ }
    }
    const page = await ctx.newPage();
    if (cfg.headers && Object.keys(cfg.headers).length) {
      await page.setExtraHTTPHeaders(cfg.headers);
    }
    page.on("request", (r) => {
      bundle.requests.push({ url: r.url(), method: r.method(), resource_type: r.resourceType() });
    });
    page.on("response", (r) => {
      bundle.responses.push({ url: r.url(), status: r.status() });
    });
    await page.goto(cfg.url, { waitUntil: "load", timeout: 30000 });
    bundle.html = await page.content();
    bundle.title = await page.title();
    bundle.final_url = page.url();
    bundle.cookies = await ctx.cookies();
    try {
      bundle.local_storage = await page.evaluate(
        "Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))",
      );
    } catch { /* ignore */ }
    try {
      bundle.session_storage = await page.evaluate(
        "Object.fromEntries(Object.keys(sessionStorage).map(k => [k, sessionStorage.getItem(k)]))",
      );
    } catch { /* ignore */ }
    try {
      bundle.scroll = await page.evaluate(
        "({ scrollHeight: document.body.scrollHeight, innerHeight: window.innerHeight })",
      );
    } catch { /* ignore */ }
    bundle.ok = true;
  } catch (e) {
    bundle.error = e && e.message ? String(e.message) : String(e);
  } finally {
    if (browser) {
      try { await browser.close(); } catch { /* ignore */ }
    }
  }
  process.stdout.write(JSON.stringify(bundle));
}

main();
