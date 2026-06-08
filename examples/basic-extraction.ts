/**
 * Basic extraction — run the canonical pipeline over an input source.
 *   npx tsx examples/basic-extraction.ts
 */
import { runCanonicalPipeline } from "webweavex";

const result = await runCanonicalPipeline({ source: "notes.txt", sourceType: "text" });
console.log("ingestion type:", result.ingestion.type);
console.log("bounded:", (result as { bounded?: boolean }).bounded);
