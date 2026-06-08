/**
 * Converted from Python: core/browser/dom_stabilization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHash, computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";

let _UUID_RE: any = py.regex("[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", "i");
let _TIMESTAMP_RE: any = py.regex("\\b\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?(?:Z|[+-]\\d{2}:?\\d{2})?\\b", "");
let _EPOCH_MS_RE: any = py.regex("\\b1[0-9]{12,13}\\b", "");
let _REACT_KEY_RE: any = py.regex("data-react(?:id|root|helmet|fiber|scroll|strictmode)?=\"[^\"]*\"", "i");
let _VUE_KEY_RE: any = py.regex("data-v-[a-z0-9]+=\"[^\"]*\"", "i");
let _ANGULAR_RE: any = py.regex("ng-version=\"[^\"]*\"|_ngcontent-[^=]+=\"[^\"]*\"", "i");
let _HYDRATION_RE: any = py.regex("data-(?:hydration|stale|server-rendered|reactroot|nextjs-scroll-focus|nuxt)(?:-id)?=\"[^\"]*\"", "i");
let _NONCE_RE: any = py.regex("(?:nonce|csp-nonce|data-nonce|integrity)=\"[^\"]*\"", "i");
let _DYNAMIC_ATTR_RE: any = py.regex("\\s(?:data-(?:vm|gh|turbo|pjax|analytics|ga|gtm|session|request-id|view-component|hydro-click|hovercard-url|octo-click|turbo-permanent|csrf|catalyst|random|app|client|feature|testid|token)|aria-(?:busy|live)=\"[^\"]*\"|style=\"[^\"]*\")", "i");
let _CSRF_META_RE: any = py.regex("<meta[^>]+(?:csrf-token|authenticity-token|nonce)[^>]*>", "i");
let _SCRIPT_BLOB_RE: any = py.regex("<script[^>]*>.*?</script>", "is");
let _STYLE_BLOB_RE: any = py.regex("<style[^>]*>.*?</style>", "is");
let _COMMENT_RE: any = py.regex("<!--.*?-->", "s");
let _BASE64_BLOB_RE: any = py.regex("[A-Za-z0-9+/]{40,}={0,2}", "");
let _SRCSET_RE: any = py.regex("srcset=\"[^\"]*\"", "i");
let _TAG_ATTR_RE: any = py.regex("<([a-zA-Z][a-zA-Z0-9]*)((?:\\s[^>]+)?)>", "");
export function _normalizeAttributes(attr_blob: any): any {
  if ((!py.truthy(attr_blob) || !py.truthy(py.strip(attr_blob)))) {
    return "";
  }
  var pairs: any[] = [];
  var match: any;
  for (match of py.iter(py.reFinditer("([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:=(?:\"([^\"]*)\"|\\'([^\\']*)\\'|([^\\s>]+)))?", attr_blob, ""))) {
    var name: any = String(match.group(1)).toLowerCase();
    var value: any = py.or2(match.group(2), () => (py.or2(match.group(3), () => (py.or2(match.group(4), () => (""))))));
    if (py.truthy(py.startswith(name, "on"))) {
      continue;
    }
    py.listAppend(pairs, [name, value]);
  }
  py.sortInPlace(pairs, {key: ((p: any) => [py.at(p, 0), py.at(p, 1)]) as (item: any) => any});
  return py.join(" ", py.iter(pairs).map(([n, v]: any) => (py.truthy(v) ? `${py.toStr(n)}="${py.toStr(v)}"` : n)));
}
export function _compactDom(html: any): any {
  var text: any = _COMMENT_RE.sub("", html);
  text = py.reSub(">\\s+<", "><", text, 0, "");
  text = py.reSub("\\s+", " ", text, 0, "");
  function _sortTag(match: any): any {
    var tag: any = String(match.group(1)).toLowerCase();
    var attrs: any = _normalizeAttributes(py.or2(match.group(2), () => ("")));
    return `<${py.toStr(tag)}${py.toStr((py.truthy(attrs) ? py.add(" ", attrs) : ""))}>`;
  }
  return py.strip(_TAG_ATTR_RE.sub(_sortTag, text));
}
export function stabilizeDomHtml(html: any): any {
  var original_len: any = py.len(html);
  var text: any = html;
  var replacements: any = {"uuids": 0, "timestamps": 0, "epoch_ms": 0, "react_keys": 0, "vue_keys": 0, "angular_keys": 0, "hydration": 0, "nonces": 0, "dynamic_attrs": 0, "script_blobs": 0, "style_blobs": 0, "base64_blobs": 0, "srcset": 0};
  function _subCount(pattern: any, repl: any, key: any): any {
    const _d1 = py.iter(pattern.subn(repl, text)) as any[];
    text = _d1[0];
    var n: any = _d1[1];
    py.setItem(replacements, key, n);
  }
  _subCount(_UUID_RE, "00000000-0000-4000-8000-000000000000", "uuids");
  _subCount(_TIMESTAMP_RE, "1970-01-01T00:00:00Z", "timestamps");
  _subCount(_EPOCH_MS_RE, "0", "epoch_ms");
  _subCount(_REACT_KEY_RE, "data-reactid=\"stable\"", "react_keys");
  _subCount(_VUE_KEY_RE, "data-v-stable=\"1\"", "vue_keys");
  _subCount(_ANGULAR_RE, "ng-version=\"stable\"", "angular_keys");
  _subCount(_HYDRATION_RE, "data-hydration=\"stable\"", "hydration");
  _subCount(_NONCE_RE, "nonce=\"stable\"", "nonces");
  _subCount(_DYNAMIC_ATTR_RE, "", "dynamic_attrs");
  _subCount(_SCRIPT_BLOB_RE, "<script></script>", "script_blobs");
  _subCount(_STYLE_BLOB_RE, "<style></style>", "style_blobs");
  _subCount(_CSRF_META_RE, "<meta>", "dynamic_attrs");
  _subCount(_BASE64_BLOB_RE, "BASE64STABLE", "base64_blobs");
  _subCount(_SRCSET_RE, "srcset=\"stable\"", "srcset");
  text = _compactDom(text);
  var meta: any = {"original_bytes": original_len, "stabilized_bytes": py.len(text), "replacements": replacements, "stabilized_hash": computeKaalkaHash(py.slice(text, null, 1000000)), "bounded": true};
  return [text, meta];
}
export function computeStableDomHash(html: any): any {
  const _d2 = py.iter(stabilizeDomHtml(html)) as any[];
  var stable: any = _d2[0];
  var _: any = _d2[1];
  return computeKaalkaHash(py.slice(stable, null, 1000000));
}
export function stabilizeExtractionPayload(extraction: any): any {
  if (!((extraction !== null && typeof extraction === "object" && !Array.isArray(extraction) && !(extraction instanceof Set) && !(extraction instanceof Map)))) {
    return {"bounded": true};
  }
  var stable: any = Object.fromEntries(py.iter(py.sorted(py.items(extraction))).filter(([k, v]: any) => !py.contains(["timestamp", "fetched_at", "nonce", "request_id", "generated_at", "updated_at"], k)).map(([k, v]: any) => ([k, v] as [any, any])));
  var links: any = py.get(stable, "links", py.get(stable, "anchors", []));
  if ((Array.isArray(links))) {
    function _linkKey(item: any): any {
      if (((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map)))) {
        return [py.toStr(py.get(item, "href", py.get(item, "url", ""))), py.toStr(py.get(item, "text", ""))];
      }
      return [py.toStr(item), ""];
    }
    py.setItem(stable, "links", py.sorted(links, {key: (_linkKey) as (item: any) => any}));
  }
  py.setItem(stable, "bounded", true);
  return stable;
}
export function stableBrowserIrFingerprint(url: any, title: any, dom_stabilization: any, extraction: any, authenticated: any = false): any {
  return computeKaalkaHashPayload({"url": url, "title": title, "dom_hash": py.get(dom_stabilization, "stabilized_hash", ""), "links": py.slice(py.get(extraction, "links", []), null, 200), "authenticated": authenticated});
}
export { computeKaalkaHash, computeKaalkaHashPayload };
