import { describe, expect, it, vi } from "vitest";

vi.mock("playwright", () => ({
  chromium: {
    launch: vi.fn(async () => ({
      newPage: vi.fn(async () => ({
        goto: vi.fn(),
        content: vi.fn(async () => "<html>ok</html>"),
        url: vi.fn(() => "https://example.com"),
      })),
      close: vi.fn(),
    })),
  },
}));

describe("renderPage", () => {
  it("renders with playwright mock", async () => {
    const { renderPage } = await import("../../src/browser/renderPage.js");
    const r = await renderPage("https://example.com");
    expect(r.available).toBe(true);
    expect(r.html).toContain("ok");
  });
});
