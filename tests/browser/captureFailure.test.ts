import { describe, expect, it, vi } from "vitest";

vi.mock("playwright", () => ({
  chromium: {
    launch: vi.fn(async () => {
      throw new Error("no browser");
    }),
  },
}));

describe("captureRuntime failure", () => {
  it("graceful when playwright fails", async () => {
    const { captureRuntime, captureDom } = await import("../../src/browser/captureRuntime.js");
    const c = await captureRuntime("https://example.com");
    expect(c.available).toBe(false);
    const d = await captureDom("https://example.com");
    expect(d.dom_hash).toBeTruthy();
  });
});
