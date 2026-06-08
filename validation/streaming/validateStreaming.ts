import { makeStreamEvent } from "../../src/streaming/streamCapture.js";
import { replayStreamEvents } from "../../src/streaming/streamReplay.js";

const events = [makeStreamEvent(1, "api", "in", "{}", "c1")];
const replay = replayStreamEvents(events);

const results = {
  event_id: events[0]!.id === "stream_1",
  replay_equivalent: replay.equivalent === true,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
