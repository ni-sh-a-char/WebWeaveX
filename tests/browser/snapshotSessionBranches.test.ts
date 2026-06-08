import { describe, expect, it, vi } from "vitest";
import { captureRuntimeSnapshot } from "../../src/browser/runtimeSnapshot.js";
import { createRuntimeSession } from "../../src/browser/runtimeSession.js";

vi.mock("../../src/browser/captureRuntime.js", () => ({
  captureRuntime: vi.fn(async () => ({
    available: true,
    url: "https://example.com",
    dom_hash: "abc",
    storage: { localStorage: {}, sessionStorage: {} },
    network: [],
    routes: ["/"],
    bounded: true,
  })),
}));

describe("runtime snapshot session branches", () => {
  it("includes session_id when session provided", async () => {
    const snap = await captureRuntimeSnapshot(
      "https://example.com",
      2,
      createRuntimeSession({ session_id: "sess-branch" }),
    );
    expect(snap.session_id).toBeTruthy();
    expect(snap.captured_at_tick).toBe(2);
  });

  it("omits session_id when session absent", async () => {
    const snap = await captureRuntimeSnapshot("https://example.com", 0);
    expect(snap.session_id).toBeUndefined();
    expect(snap.snapshot_id).toBeTruthy();
  });
});
