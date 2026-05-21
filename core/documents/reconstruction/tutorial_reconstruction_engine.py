from __future__ import annotations
import re

def reconstruct_tutorial(text: str):
    steps = sorted(set(re.findall(r'^\s*\d+\.\s+(.+)$', text or '', flags=re.MULTILINE)))
    flow = [{"from": steps[i], "to": steps[i+1]} for i in range(max(0, len(steps)-1))]
    return {"steps": steps, "flow": flow}
