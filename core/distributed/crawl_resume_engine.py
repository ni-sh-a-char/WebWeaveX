from __future__ import annotations
import json
def resume(checkpoint_text:str):
    return json.loads(checkpoint_text or "{}")
