export type RenderResult = {
  available: boolean;
  html: string;
  url: string;
  bounded: boolean;
  error?: string;
};

export async function renderPage(url: string): Promise<RenderResult> {
  try {
    const { chromium } = await import("playwright");
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30_000 });
    const html = await page.content();
    const finalUrl = page.url();
    await browser.close();
    return { available: true, html, url: finalUrl, bounded: true };
  } catch (err) {
    return {
      available: false,
      html: "",
      url,
      bounded: true,
      error: err instanceof Error ? err.message : String(err),
    };
  }
}
