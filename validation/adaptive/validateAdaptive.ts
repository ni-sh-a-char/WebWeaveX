import { runAdaptiveExtraction } from "../../src/adaptive/adaptiveOrchestrator.js";

const out = runAdaptiveExtraction("#btn", "<div id='btn'>Go</div>", [
  { tag: "div", text: "Go", attrs: { id: "btn" } },
]);

const results = {
  stabilized: typeof out.stabilized_html === "string",
  healed: String(out.healed_selector).length > 0,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
