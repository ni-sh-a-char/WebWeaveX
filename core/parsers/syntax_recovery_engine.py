from __future__ import annotations


def recover_syntax(source: str, language: str) -> str:
    text = source or ""
    if language.lower() == "python":
        lines = text.splitlines()
        repaired = []
        balance = 0
        for ln in lines:
            repaired.append(ln.rstrip())
            balance += ln.count("(") - ln.count(")")
        while balance > 0:
            repaired.append(")")
            balance -= 1
        return "\n".join(repaired)
    return text
