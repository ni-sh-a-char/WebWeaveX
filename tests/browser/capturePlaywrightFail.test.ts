import { describe, expect, it, vi } from "vitest";

vi.mock("../../src/browser/renderPage.js", () => ({
  renderPage: vi.fn(async (url: string) => ({
    available: true,
    html: "<div>fallback</div>",
    url,
    bounded: true,
  })),
}));

vi.mock("playwright", () => ({
  chromium: {
    launch: vi.fn(async () => {
      throw new Error("playwright missing");
    }),
  },
}));

describe("captureRuntime playwright failure", () => {
  it(
    "falls back when playwright throws",
    async () => {
    const { captureRuntime } = await import("../../src/browser/captureRuntime.js");
    const c = await captureRuntime("https://example.com");
    expect(c.available).toBe(false);
    expect(c.dom_hash).toBeTruthy();
    expect(c.routes).toContain("https://example.com");
    },
    15_000,
  );
});
