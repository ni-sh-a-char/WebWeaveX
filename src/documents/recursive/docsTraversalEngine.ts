/**
 * Converted from Python: core/documents/recursive/docs_traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { discoverLinks } from "../../crawling/traversalEngine.js";

export function traverseDocs(base_url: any, text: any): any {
  return {"links": discoverLinks(base_url, text)};
}
export { discoverLinks };
