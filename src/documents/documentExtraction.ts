const URL_RE = /https?:\/\/[^\s)]+/gi;
const DOI_RE = /doi:\s*[^\s)]+/gi;
const CITE_RE = /\b[A-Z][a-z]+(?:\s+et\s+al\.)?\s*\(\d{4}\)/g;

export function extractDocumentStructure(markdown: string): Record<string, unknown> {
  const headings: Array<Record<string, unknown>> = [];
  for (const line of markdown.split("\n")) {
    const m = /^(#{1,6})\s+(.+)$/.exec(line.trim());
    if (m) headings.push({ level: m[1]!.length, text: m[2]!.trim() });
  }
  const links = [...markdown.matchAll(URL_RE)].map((m) => ({ href: m[0] }));
  return { headings, links, bounded: true };
}

export function extractCitations(text: string): Record<string, unknown> {
  const citations = [
    ...[...text.matchAll(CITE_RE)].map((m) => ({ kind: "author_year", raw: m[0] })),
    ...[...text.matchAll(DOI_RE)].map((m) => ({ kind: "doi", raw: m[0] })),
  ];
  return { citations, bounded: true };
}
