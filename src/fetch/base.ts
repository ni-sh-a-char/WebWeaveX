/**
 * Converted from Python: core/fetch/base.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class FetchResponse {
  declare source: any;
  declare url: any;
  declare status_code: any;
  declare content_type: any;
  declare text: any;
  declare ok: any;
  declare error: any;
  declare metadata: any;
  constructor(source: any, url: any, status_code: any, content_type: any, text: any, ok: any, error: any, metadata: any) {
    this.source = source;
    this.url = url;
    this.status_code = status_code;
    this.content_type = content_type;
    this.text = text;
    this.ok = ok;
    this.error = error;
    this.metadata = metadata;
  }
  to_dict(): any {
    var data: any = py.deepcopy(this);
    py.setItem(data, "metadata", py.pyDict(py.sorted(py.items(py.or2(this.metadata, () => ({}))))));
    py.setItem(data, "fingerprint", py.hashNew("sha256", py.encode(`${py.toStr(this.source)}|${py.toStr(this.url)}|${py.toStr(this.status_code)}|${py.toStr(this.content_type)}|${py.toStr(this.text)}`, "utf-8")).hexdigest());
    return data;
  }
}
