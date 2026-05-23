import { describe, expect, it } from "vitest";
import {
  computeSpaFingerprint,
  computeStableDomHash,
  stabilizeDomHtml,
} from "../../src/determinism/domStabilization.js";

describe("DOM stabilization", () => {
  it("strips framework noise and stabilizes scripts", () => {
    const html = '<div data-reactroot="1" nonce="n"><script>volatile()</script>Hi</div>';
    const s = stabilizeDomHtml(html);
    expect(s).not.toContain("nonce=");
    expect(s).not.toContain("volatile()");
    expect(s).toContain("stabilized");
  });

  it("stable dom hash", () => {
    const h1 = computeStableDomHash("<p>a</p>");
    const h2 = computeStableDomHash("<p>a</p>");
    expect(h1).toBe(h2);
    expect(computeSpaFingerprint("<p>a</p>")).toBe(h1);
  });
});
