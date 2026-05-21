from __future__ import annotations
import re
def sanitize_html(text:str):
    return re.sub(r"<script.*?>.*?</script>","", text or "", flags=re.I|re.S)
