/**
 * Converted from Python: core/streaming/stream_parser.py
 * @generated — WebWeaveX python→javascript library port
 */

import { chunkText } from "./chunkEngine.js";
import { enforceMemoryLimit } from "./memoryGuard.js";

export function parseStream(text: any, chunk_size: any = 4096): any {
  var safe: any = enforceMemoryLimit(text);
  return chunkText(safe, chunk_size);
}
export { chunkText, enforceMemoryLimit };
