import { extractCitations, extractDocumentStructure } from "../../src/documents/documentExtraction.js";

const doc = extractDocumentStructure("# Title\n\nSee https://example.com\n");
const cites = extractCitations("Smith (2020) doi:10.1000/xyz");

const results = {
  headings: (doc.headings as unknown[]).length > 0,
  links: (doc.links as unknown[]).length > 0,
  citations: (cites.citations as unknown[]).length > 0,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
