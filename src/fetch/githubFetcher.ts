/**
 * Converted from Python: core/fetch/github_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { fetchSync, fetchAsync } from "./httpFetcher.js";

export function fetchGithubSync(url: any): any {
  var data: any = fetchSync(url);
  py.setItem(data, "source", "github");
  return data;
}
export async function fetchGithubAsync(url: any): Promise<any> {
  var data: any = await fetchAsync(url);
  py.setItem(data, "source", "github");
  return data;
}
export { fetchAsync, fetchSync };
