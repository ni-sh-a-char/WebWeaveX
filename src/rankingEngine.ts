/**
 * Converted from Python: core/ranking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function _scoreText(content: any): any {
  if (!((content !== null && typeof content === "object" && !Array.isArray(content) && !(content instanceof Set) && !(content instanceof Map)))) {
    return 0;
  }
  var text_len: any = py.get(py.get(content, "metadata", {}), "text_length", 0);
  if ((text_len > 2000)) {
    return 5;
  } else if ((text_len > 1000)) {
    return 4;
  } else if ((text_len > 500)) {
    return 3;
  } else if ((text_len > 200)) {
    return 2;
  } else if ((text_len > 50)) {
    return 1;
  }
  return 0;
}
export function _scoreCode(content: any): any {
  if (!((content !== null && typeof content === "object" && !Array.isArray(content) && !(content instanceof Set) && !(content instanceof Map)))) {
    return 0;
  }
  var code_blocks: any = py.get(py.get(content, "metadata", {}), "code_blocks", 0);
  if ((code_blocks >= 3)) {
    return 5;
  } else if (py.eq(code_blocks, 2)) {
    return 4;
  } else if (py.eq(code_blocks, 1)) {
    return 3;
  }
  return 0;
}
export function _scoreRecovery(recovered: any): any {
  if (!((recovered !== null && typeof recovered === "object" && !Array.isArray(recovered) && !(recovered instanceof Set) && !(recovered instanceof Map)))) {
    return 0;
  }
  var count: any = py.get(recovered, "recovered_count", 0);
  if ((count >= 3)) {
    return 5;
  } else if (py.eq(count, 2)) {
    return 3;
  } else if (py.eq(count, 1)) {
    return 1;
  }
  return 0;
}
export function _scoreSource(source: any, keywords: any = ""): any {
  var base: any = 0;
  if (py.eq(source, "github")) {
    base = 5;
  } else if (py.eq(source, "stackoverflow")) {
    base = 4;
  } else if (py.eq(source, "codepen")) {
    base = 3;
  } else if (py.eq(source, "docs")) {
    base = 4;
  } else if (py.eq(source, "web")) {
    base = 2;
  } else if (py.eq(source, "news")) {
    base = 1;
  }
  var keywords_lower: any = String(keywords).toLowerCase();
  if ((py.contains(keywords_lower, "code") || py.contains(keywords_lower, "api"))) {
    if (py.eq(source, "github")) {
      base = py.add(base, 2);
    }
  } else if ((py.contains(keywords_lower, "error") || py.contains(keywords_lower, "fix"))) {
    if (py.eq(source, "stackoverflow")) {
      base = py.add(base, 2);
    }
  }
  return py.min([base, 7]);
}
export function computeScore(item: any, keywords: any = ""): any {
  var base: any = py.get(item, "base", {});
  var recovered: any = py.get(item, "recovered");
  var source: any = py.get(item, "source", "");
  var score: any = 0;
  score = py.add(score, _scoreText(base));
  score = py.add(score, _scoreCode(base));
  score = py.add(score, _scoreRecovery(recovered));
  score = py.add(score, _scoreSource(source, keywords));
  return py.min([score, 10]);
}
export function rankResults(adaptive_output: any): any {
  if (!((adaptive_output !== null && typeof adaptive_output === "object" && !Array.isArray(adaptive_output) && !(adaptive_output instanceof Set) && !(adaptive_output instanceof Map)))) {
    throw py.err("TypeError", "adaptive_output must be dict");
  }
  if (!py.contains(adaptive_output, "adaptive_results")) {
    throw py.err("ValueError", "Missing adaptive_results");
  }
  if (!(Array.isArray(py.at(adaptive_output, "adaptive_results")))) {
    throw py.err("TypeError", "adaptive_results must be a list");
  }
  var ranked: any[] = [];
  var item: any;
  for (item of py.iter(py.at(adaptive_output, "adaptive_results"))) {
    if (!((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map)))) {
      continue;
    }
    var keywords: any = py.get(item, "query", "");
    var score: any = computeScore(item, keywords);
    py.listAppend(ranked, {...(item), "score": score});
  }
  if (!py.truthy(ranked)) {
    py.listAppend(ranked, {"source": "fallback", "url": "", "base": {"text": "fallback", "code": [], "metadata": {"text_length": 1, "code_blocks": 0}}, "recovered": {"recovered": [], "recovered_count": 0}, "input_signature": "", "score": 0});
  }
  var ranked_sorted: any = py.sorted(ranked, {key: ((x: any) => [(-py.at(x, "score")), py.get(x, "source", ""), py.get(x, "url", "")]) as (item: any) => any});
  var top_result: any = (py.truthy(ranked_sorted) ? py.at(ranked_sorted, 0) : {"source": "none", "url": "", "base": {"text": "", "code": [], "metadata": {"text_length": 0, "code_blocks": 0}}, "recovered": {"recovered": [], "recovered_count": 0}, "input_signature": ""});
  return {"ranked_results": ranked_sorted, "top_result": top_result, "total": py.len(ranked_sorted), "version": "v1_phase_8"};
}
export function validateRankingEngine(): any {
  var test_input: any = {"adaptive_results": [{"source": "github", "url": "a", "base": {"metadata": {"text_length": 1500, "code_blocks": 2}}, "recovered": null}, {"source": "web", "url": "b", "base": {"metadata": {"text_length": 300, "code_blocks": 0}}, "recovered": null}]};
  var result: any = rankResults(test_input);
  if (!((result !== null && typeof result === "object" && !Array.isArray(result) && !(result instanceof Set) && !(result instanceof Map)))) {
    throw py.err("RuntimeError", "Invalid output");
  }
  if (!py.contains(result, "ranked_results")) {
    throw py.err("RuntimeError", "Missing ranked_results");
  }
  if (!py.eq(py.at(py.at(result, "top_result"), "source"), "github")) {
    throw py.err("RuntimeError", "Ranking failed");
  }
  return true;
}
