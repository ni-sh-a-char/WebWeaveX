import { describe, expect, it, vi } from "vitest";
import { extractWeb } from "../../src/browser/extractWeb.js";

vi.mock("../../src/browser/captureRuntime.js", () => ({
  captureRuntime: vi.fn(async () => ({
    available: true,
    url: "https://example.com",
    dom_hash: "abc",
    storage: { localStorage: {}, sessionStorage: {} },
    network: [],
    routes: ["https://example.com"],
    bounded: true,
  })),
}));

describe("extractWeb", () => {
  it("returns bounded envelope", async () => {
    const out = await extractWeb("https://example.com");
    expect(out.bounded).toBe(true);
    expect(out.unified_runtime_graph?.nodes.length).toBeGreaterThan(0);
  });
});
