import requests
import time
from .rate_limiter import RateLimiter

def fetch_url(url, context):
    from .config import CONFIG

    try:
        if context["meta"]["deterministic_mode"]:
            base_url = url.split("://")[-1].split("/")[0] if url else "example"
            return f"""<html><head><title>{base_url}</title></head><body><h1>{base_url}</h1><p>Deterministic content for {url}</p></body></html>"""

        rate_limiter = context["crawl"].get("rate_limiter")
        if rate_limiter is None:
            rate_limiter = RateLimiter(5)
            context["crawl"]["rate_limiter"] = rate_limiter

        rate_limiter.wait()
        delay = CONFIG.get("crawl_delay", 0.5)
        time.sleep(delay)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        context.setdefault("meta", {})
        context["meta"]["last_error"] = str(e)
        return ""
