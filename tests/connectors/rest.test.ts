import { describe, expect, it, vi } from "vitest";
import { extractRestRuntime } from "../../src/connectors/restConnector.js";

describe("rest connector", () => {
  it("fetch ok", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({ ok: true }) as Response),
    );
    const r = await extractRestRuntime("https://example.com");
    expect(r.available).toBe(true);
    vi.unstubAllGlobals();
  });

  it("fetch fail", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw new Error("net");
    }));
    const r = await extractRestRuntime("https://example.com");
    expect(r.available).toBe(false);
    vi.unstubAllGlobals();
  });
});
