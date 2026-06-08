/**
 * Converted from Python: core/fetch/stackoverflow_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { fetchSync, fetchAsync } from "./httpFetcher.js";

export function fetchStackoverflowSync(url: any): any {
  var data: any = fetchSync(url);
  py.setItem(data, "source", "stackoverflow");
  return data;
}
export async function fetchStackoverflowAsync(url: any): Promise<any> {
  var data: any = await fetchAsync(url);
  py.setItem(data, "source", "stackoverflow");
  return data;
}
export { fetchAsync, fetchSync };
