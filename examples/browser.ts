import { extractWeb } from "../src/index.js";

const out = await extractWeb("https://example.com");
console.log("bounded:", out.bounded, "nodes:", out.unified_runtime_graph?.nodes.length);
