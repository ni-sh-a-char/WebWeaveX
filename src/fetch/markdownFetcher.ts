/**
 * Converted from Python: core/fetch/markdown_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { fetchSync, fetchAsync } from "./httpFetcher.js";

export function fetchMarkdownSync(url: any): any {
  var data: any = fetchSync(url);
  py.setItem(data, "source", "markdown");
  return data;
}
export async function fetchMarkdownAsync(url: any): Promise<any> {
  var data: any = await fetchAsync(url);
  py.setItem(data, "source", "markdown");
  return data;
}
export { fetchAsync, fetchSync };
