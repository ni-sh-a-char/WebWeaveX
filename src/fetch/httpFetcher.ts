/**
 * Converted from Python: core/fetch/http_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { FetchResponse } from "./base.js";

export let DEFAULT_TIMEOUT: any = py.F(12.0);
export let DEFAULT_RETRIES: any = 2;
export let UA: any = "WebWeaveX/1.1 (+https://github.com/PIYUSH-MISHRA-00)";
export let DEFAULT_ACCEPT: any = "text/html,application/json,text/plain,application/xml;q=0.9,*/*;q=0.8";
export function _response(source: any, url: any, status_code: any, content_type: any, text: any, error: any = ""): any {
  return new FetchResponse(source, url, status_code, py.or2(content_type, () => ("text/plain")), py.or2(text, () => ("")), py.and2(((200 <= status_code) && (status_code < 400)), () => (!py.truthy(error))), error, {"length": py.toStr(py.len(py.or2(text, () => (""))))}).to_dict();
}
export function fetchSync(url: any, timeout: any = DEFAULT_TIMEOUT, retries: any = DEFAULT_RETRIES): any {
  var last_err: any = "";
  var _: any;
  for (_ = 0; _ < py.add(py.max([retries, 0]), 1); _++) {
    try {
      var res: any = py.requestsGet(url, {"timeout": timeout, "headers": {"User-Agent": UA, "Accept": DEFAULT_ACCEPT, "Accept-Encoding": "identity"}, "allow_redirects": true});
      if (py.eq(res.status_code, 429)) {
        continue;
      }
      return _response("http", url, res.status_code, py.get(res.headers, "content-type", ""), res.text);
    } catch (exc: any) {
      last_err = py.toStr(exc);
    }
  }
  return _response("http", url, 0, "text/plain", "", last_err);
}
export async function fetchAsync(url: any, timeout: any = DEFAULT_TIMEOUT, retries: any = DEFAULT_RETRIES): Promise<any> {
  var last_err: any = "";
  var _: any;
  for (_ = 0; _ < py.add(py.max([retries, 0]), 1); _++) {
    try {
      var client: any = py.httpxAsyncClient({"timeout": timeout, "headers": {"User-Agent": UA, "Accept": DEFAULT_ACCEPT, "Accept-Encoding": "identity"}, "follow_redirects": true, "limits": {"max_connections": 20, "max_keepalive_connections": 10}});
      var res: any = await py.get(client, url);
      if (py.eq(res.status_code, 429)) {
        continue;
      }
      return _response("http", url, res.status_code, py.get(res.headers, "content-type", ""), res.text);
    } catch (exc: any) {
      last_err = py.toStr(exc);
    }
  }
  return _response("http", url, 0, "text/plain", "", last_err);
}
export { FetchResponse };
