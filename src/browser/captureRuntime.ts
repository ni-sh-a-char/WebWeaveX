import { computeStableDomHash } from "../determinism/domStabilization.js";
import { renderPage } from "./renderPage.js";

export type CapturedRuntime = {
  available: boolean;
  url: string;
  dom_hash: string;
  storage: { localStorage: Record<string, string>; sessionStorage: Record<string, string> };
  network: Array<{ url: string; method: string }>;
  routes: string[];
  bounded: boolean;
};

export async function captureRuntime(url: string): Promise<CapturedRuntime> {
  const rendered = await renderPage(url);
  if (!rendered.available) {
    return {
      available: false,
      url,
      dom_hash: computeStableDomHash(""),
      storage: { localStorage: {}, sessionStorage: {} },
      network: [],
      routes: [],
      bounded: true,
    };
  }

  try {
    const { chromium } = await import("playwright");
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    const network: Array<{ url: string; method: string }> = [];
    page.on("request", (req) => {
      network.push({ url: req.url(), method: req.method() });
    });
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30_000 });
    const storage = await page.evaluate(() => ({
      localStorage: { ...localStorage },
      sessionStorage: { ...sessionStorage },
    }));
    const html = await page.content();
    const routes = [page.url()];
    await browser.close();
    network.sort((a, b) => `${a.method}|${a.url}`.localeCompare(`${b.method}|${b.url}`));
    return {
      available: true,
      url: rendered.url,
      dom_hash: computeStableDomHash(html),
      storage,
      network,
      routes,
      bounded: true,
    };
  } catch {
    return {
      available: false,
      url,
      dom_hash: computeStableDomHash(rendered.html),
      storage: { localStorage: {}, sessionStorage: {} },
      network: [],
      routes: [url],
      bounded: true,
    };
  }
}

export async function captureDom(url: string): Promise<{ html: string; dom_hash: string }> {
  const r = await renderPage(url);
  return { html: r.html, dom_hash: computeStableDomHash(r.html) };
}
