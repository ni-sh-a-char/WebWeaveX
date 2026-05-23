import { describe, expect, it, vi } from "vitest";

const page = {
  goto: vi.fn(),
  content: vi.fn(async () => "<div>hi</div>"),
  url: vi.fn(() => "https://example.com"),
  evaluate: vi.fn(async () => ({ localStorage: {}, sessionStorage: {} })),
  on: vi.fn(),
};

vi.mock("playwright", () => ({
  chromium: {
    launch: vi.fn(async () => ({
      newPage: vi.fn(async () => page),
      close: vi.fn(),
    })),
  },
}));

describe("captureRuntime", () => {
  it("captures runtime", async () => {
    const { captureRuntime, captureDom } = await import("../../src/browser/captureRuntime.js");
    const c = await captureRuntime("https://example.com");
    expect(c.bounded).toBe(true);
    expect(c.dom_hash).toBeTruthy();
    const d = await captureDom("https://example.com");
    expect(d.dom_hash).toBeTruthy();
  });
});
