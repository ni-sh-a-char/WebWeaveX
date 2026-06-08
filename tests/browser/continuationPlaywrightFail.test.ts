import { describe, expect, it, vi } from "vitest";
import { extractWithSession } from "../../src/browser/runtimeContinuation.js";
import { createRuntimeSession } from "../../src/browser/runtimeSession.js";

vi.mock("../../src/browser/captureRuntime.js", () => ({
  captureRuntime: vi.fn(async () => ({
    available: true,
    url: "https://example.com",
    dom_hash: "h",
    storage: { localStorage: {}, sessionStorage: {} },
    network: [],
    routes: ["/"],
    bounded: true,
  })),
  captureDom: vi.fn(async () => ({ html: "<p/>", dom_hash: "h" })),
}));

vi.mock("playwright", () => ({
  chromium: {
    launch: vi.fn(async () => {
      throw new Error("playwright unavailable");
    }),
  },
}));

describe("runtime continuation playwright failure", () => {
  it("sets continuation false when playwright throws", async () => {
    const session = createRuntimeSession({
      cookies: [{ name: "c", value: "1", domain: "example.com", path: "/" }],
      localStorage: { theme: "dark" },
    });
    const out = await extractWithSession("https://example.com", session, 0);
    const cont = (out.runtime as Record<string, unknown>).session as Record<string, unknown>;
    expect(cont.continuation).toBe(false);
    expect(out.bounded).toBe(true);
  });
});
