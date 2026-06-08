/**
 * Converted from Python: core/extract/pipeline.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractArchitecture } from "./architectureExtractor.js";
import { extractCodeFeatures } from "./codeExtractor.js";
import { extractDependencies } from "./dependencyExtractor.js";
import { _merge, enrichExtraction } from "./enrichmentEngine.js";
import { extractHtml } from "./htmlExtractor.js";
import { extractMarkdown } from "./markdownExtractor.js";
import { extractMetadata } from "./metadataExtractor.js";
import { extractRepositoryData } from "./repositoryExtractor.js";
import { extractRepositoryIntelligence } from "./repositoryIntelligence.js";
import { extractRepositoryV2 } from "./advanced/repositoryExtractorV2.js";
import { extractApiV2 } from "./advanced/apiExtractor.js";
import { extractDependenciesV2 } from "./advanced/dependencyExtractorV2.js";
import { extractDocsV2 } from "./advanced/docsExtractorV2.js";
import { extractArchitectureV2 } from "./advanced/architectureExtractorV2.js";
import { fetchAsync, fetchSync } from "../fetch/httpFetcher.js";
import { fetchRaw } from "../fetch/rawFetcher.js";
import { complete as groqComplete } from "../llm/groqAdapter.js";
import { isolateLlm } from "../llm/sandbox.js";
import { normalizeOutput } from "../normalize/normalizeOutput.js";
import { MAX_HTML_SIZE, enforceTextLimit } from "../security/payloadLimits.js";
import { safeHtmlText } from "../security/safeParser.js";
import { isSafeUrl } from "../security/urlValidator.js";
import { sandboxText } from "../security/hardening/index.js";
import { analyzeDocument } from "../documents/documentIntelligence.js";
import { analyzeRepository } from "../repository/repositoryIntelligence.js";

export function _isUrl(value: any): any {
  return py.or2(py.startswith(value, "http://"), () => (py.startswith(value, "https://")));
}
export function _extractCore(text: any, source_url: any): any {
  var safe_text: any = sandboxText(enforceTextLimit(py.or2(text, () => ("")), MAX_HTML_SIZE));
  var html_text: any = safeHtmlText(safe_text);
  var merged: any = _merge(extractHtml(safe_text), extractMarkdown(safe_text), {"code": extractCodeFeatures(safe_text)}, {"dependencies": extractDependencies(safe_text)}, {"relationships": extractArchitecture(safe_text)}, {"content": extractRepositoryData(safe_text, source_url)}, {"metadata": extractMetadata(safe_text, source_url)}, extractRepositoryIntelligence(safe_text, source_url), {"content": {"repository_v2": extractRepositoryV2(safe_text)}}, {"content": {"api_surface_v2": extractApiV2(safe_text)}}, {"dependencies": {"graph_v2": extractDependenciesV2(safe_text)}}, {"content": {"docs_v2": extractDocsV2(safe_text)}}, {"relationships": {"architecture_v2": extractArchitectureV2(safe_text, source_url)}}, {"content": {"repository_intelligence_v12": analyzeRepository(safe_text, source_url)}}, {"content": {"document_intelligence_v12": analyzeDocument(safe_text)}});
  py.setItem(merged, "raw_text", py.or2(html_text, () => (safe_text)));
  py.setItem(merged, "source_url", source_url);
  var normalized: any = normalizeOutput(merged, source_url);
  return enrichExtraction(normalized, safe_text, source_url, merged);
}
export function extract(input_data: any): any {
  var cfg: any = (((input_data !== null && typeof input_data === "object" && !Array.isArray(input_data) && !(input_data instanceof Set) && !(input_data instanceof Map))) ? input_data : {"source": input_data});
  var source: any = py.toStr(py.or2(py.get(cfg, "source", ""), () => ("")));
  var llm: any = String(py.toStr(py.or2(py.get(cfg, "llm", ""), () => ("")))).toLowerCase();
  if (py.truthy(_isUrl(source))) {
    if (!py.truthy(isSafeUrl(source))) {
      var core: any = _extractCore("", source);
      py.setItem(py.at(core, "metadata"), "fetch", {"status_code": 0, "content_type": "text/plain", "ok": false, "error": "unsafe_url"});
      return core;
    }
    var fetched: any = fetchSync(source);
  } else {
    fetched = fetchRaw(source, "");
  }
  core = _extractCore(py.toStr(py.or2(py.get(fetched, "text", ""), () => (""))), (py.truthy(_isUrl(source)) ? source : ""));
  py.setItem(py.at(core, "metadata"), "fetch", Object.fromEntries(py.iter(["status_code", "content_type", "ok", "error"]).map((k: any) => ([k, py.get(fetched, k)] as [any, any]))));
  if (py.eq(llm, "groq")) {
    var llm_result: any = groqComplete(py.slice(py.at(core, "raw_text"), null, 4000), "extraction enhancement");
    var isolated: any = isolateLlm(core, llm_result);
    py.setItem(py.at(core, "metadata"), "llm", py.deepcopy(py.at(isolated, "llm")));
  }
  return core;
}
export async function extractAsync(input_data: any): Promise<any> {
  var cfg: any = (((input_data !== null && typeof input_data === "object" && !Array.isArray(input_data) && !(input_data instanceof Set) && !(input_data instanceof Map))) ? input_data : {"source": input_data});
  var source: any = py.toStr(py.or2(py.get(cfg, "source", ""), () => ("")));
  var llm: any = String(py.toStr(py.or2(py.get(cfg, "llm", ""), () => ("")))).toLowerCase();
  if (py.truthy(_isUrl(source))) {
    if (!py.truthy(isSafeUrl(source))) {
      var core: any = _extractCore("", source);
      py.setItem(py.at(core, "metadata"), "fetch", {"status_code": 0, "content_type": "text/plain", "ok": false, "error": "unsafe_url"});
      return core;
    }
    var fetched: any = await fetchAsync(source);
  } else {
    fetched = fetchRaw(source, "");
  }
  core = _extractCore(py.toStr(py.or2(py.get(fetched, "text", ""), () => (""))), (py.truthy(_isUrl(source)) ? source : ""));
  py.setItem(py.at(core, "metadata"), "fetch", Object.fromEntries(py.iter(["status_code", "content_type", "ok", "error"]).map((k: any) => ([k, py.get(fetched, k)] as [any, any]))));
  if (py.eq(llm, "groq")) {
    var llm_result: any = groqComplete(py.slice(py.at(core, "raw_text"), null, 4000), "extraction enhancement");
    var isolated: any = isolateLlm(core, llm_result);
    py.setItem(py.at(core, "metadata"), "llm", py.deepcopy(py.at(isolated, "llm")));
  }
  return core;
}
export function extractDocs(source: any): any {
  return extract(source);
}
export function extractRepo(source: any): any {
  return extract(source);
}
export { MAX_HTML_SIZE, analyzeDocument, analyzeRepository, enforceTextLimit, enrichExtraction, extractApiV2, extractArchitecture, extractArchitectureV2, extractCodeFeatures, extractDependencies, extractDependenciesV2, extractDocsV2, extractHtml, extractMarkdown, extractMetadata, extractRepositoryData, extractRepositoryIntelligence, extractRepositoryV2, fetchAsync, fetchRaw, fetchSync, groqComplete, isSafeUrl, isolateLlm, normalizeOutput, safeHtmlText, sandboxText };
