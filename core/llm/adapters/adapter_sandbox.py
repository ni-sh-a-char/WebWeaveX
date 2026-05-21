from __future__ import annotations

def sandbox_output(core_result: dict, llm_output: dict):
    out=dict(core_result)
    meta=dict(out.get('metadata',{}))
    meta['llm']=llm_output
    out['metadata']=meta
    return out
