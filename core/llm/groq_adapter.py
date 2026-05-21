from __future__ import annotations

import os
from core.llm.base_adapter import disabled_result


def complete(prompt: str, timeout: float = 10.0, task: str = "completion"):
    if os.getenv("WEBWEAVEX_DISABLE_LLM", "0") == "1":
        return disabled_result("groq", "llm_disabled")
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return disabled_result("groq", "missing_api_key")
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=os.getenv("WEBWEAVEX_GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0,
            timeout=timeout,
            messages=[
                {"role": "system", "content": f"You are a deterministic {task} assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        output = (completion.choices[0].message.content or "").strip()
        return {"provider": "groq", "enabled": True, "ok": True, "reason": "", "output": output}
    except Exception as exc:
        return disabled_result("groq", f"failure:{exc}")
