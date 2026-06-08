/**
 * Converted from Python: core/crawling/streaming_crawler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { chunkText } from "../streaming/chunkEngine.js";

export function streamCrawlText(text: any, chunk_size: any = 4096): any {
  return chunkText(py.or2(text, () => ("")), chunk_size);
}
export { chunkText };
