/**
 * Converted from Python: core/fetch/medium_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { fetchSync, fetchAsync } from "./httpFetcher.js";

export function fetchMediumSync(url: any): any {
  var data: any = fetchSync(url);
  py.setItem(data, "source", "medium");
  return data;
}
export async function fetchMediumAsync(url: any): Promise<any> {
  var data: any = await fetchAsync(url);
  py.setItem(data, "source", "medium");
  return data;
}
export { fetchAsync, fetchSync };
