from __future__ import annotations

import re


def sanitize_html_v3(html: str):
    source = html or ""
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", "", source, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"on[a-z]+\s*=\s*['\"][^'\"]*['\"]", "", cleaned, flags=re.IGNORECASE)
    return cleaned
