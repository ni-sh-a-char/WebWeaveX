import { describe, expect, it, vi } from "vitest";

vi.mock("../../src/browser/renderPage.js", () => ({
  renderPage: vi.fn(async (url: string) => ({
    available: false,
    html: "",
    url,
    bounded: true,
    error: "no browser",
  })),
}));

describe("captureRuntime failure", () => {
  it("graceful when render unavailable", async () => {
    const { captureRuntime, captureDom } = await import("../../src/browser/captureRuntime.js");
    const c = await captureRuntime("https://example.com");
    expect(c.available).toBe(false);
    const d = await captureDom("https://example.com");
    expect(d.dom_hash).toBeTruthy();
  });
});
