import { describe, expect, it } from "vitest";
import { normalizeStreamEvents, makeStreamEvent } from "../../src/streaming/streamCapture.js";
import { buildStreamTimeline, replayStreamEvents } from "../../src/streaming/streamReplay.js";
import { saveStreamRuntime, loadStreamRuntime, mergeStreamRuntimes } from "../../src/streaming/streamPersistence.js";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

describe("streaming branches", () => {
  it("normalizes unsorted events", () => {
    const events = normalizeStreamEvents([
      { timestamp: 2, source: "b", direction: "out", payload: "y", connection_id: "c" },
      { timestamp: 1, source: "a", direction: "in", payload: "x", connection_id: "c" },
    ]);
    expect(events[0]!.timestamp).toBe(1);
    const timeline = buildStreamTimeline(events);
    expect(timeline.start).toBe(1);
    expect(replayStreamEvents(events).equivalent).toBe(true);
  });

  it("persists encrypted stream runtime", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-str-"));
    const path = join(dir, "s.json");
    saveStreamRuntime(path, { events: [makeStreamEvent(0, "s", "in", "{}", "c")] }, "k");
    const loaded = loadStreamRuntime(path, "k");
    const merged = mergeStreamRuntimes(loaded, { events: [makeStreamEvent(1, "s", "out", "{}", "c")] });
    expect((merged.events as unknown[]).length).toBe(2);
    rmSync(dir, { recursive: true, force: true });
  });
});
