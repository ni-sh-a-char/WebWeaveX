#!/usr/bin/env python3
"""Generate validation/real_world/urlMatrix.json with 1000+ real URLs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "validation" / "real_world" / "urlMatrix.json"

# Real hosts per Omega directive category
HOSTS: dict[str, list[str]] = {
    "news": [
        "www.bbc.com", "www.reuters.com", "apnews.com", "www.theguardian.com", "www.nytimes.com",
        "www.washingtonpost.com", "www.npr.org", "www.aljazeera.com", "www.ft.com", "www.economist.com",
        "www.cnn.com", "www.bloomberg.com", "www.politico.com", "www.cbsnews.com", "www.nbcnews.com",
    ],
    "blogs": [
        "blog.cloudflare.com", "engineering.fb.com", "netflixtechblog.com", "stripe.com", "github.blog",
        "aws.amazon.com", "martinfowler.com", "blog.google", "openai.com", "www.docker.com",
    ],
    "government": [
        "www.usa.gov", "www.gov.uk", "europa.eu", "www.canada.ca", "www.gov.au", "www.data.gov",
        "www.nih.gov", "www.cdc.gov", "www.nasa.gov", "www.sec.gov",
    ],
    "academic": [
        "arxiv.org", "web.mit.edu", "www.stanford.edu", "www.harvard.edu", "www.berkeley.edu",
        "www.cam.ac.uk", "www.ox.ac.uk", "www.cmu.edu", "www.caltech.edu", "www.yale.edu",
    ],
    "wikipedia": [
        "en.wikipedia.org",
    ],
    "documentation": [
        "developer.mozilla.org", "nodejs.org", "docs.python.org", "www.typescriptlang.org",
        "react.dev", "kubernetes.io", "docs.docker.com", "www.rust-lang.org", "go.dev", "docs.microsoft.com",
    ],
    "forums": [
        "news.ycombinator.com", "stackoverflow.com", "www.reddit.com", "discourse.org", "meta.stackexchange.com",
    ],
    "ecommerce": [
        "www.amazon.com", "www.etsy.com", "www.shopify.com", "www.ebay.com", "www.walmart.com",
        "www.target.com", "www.bestbuy.com", "www.alibaba.com",
    ],
    "legal": [
        "www.law.cornell.edu", "www.supremecourt.gov", "www.legislation.gov.uk", "www.justice.gov",
    ],
    "scientific": [
        "www.nature.com", "www.science.org", "journals.plos.org", "www.springer.com", "www.sciencedirect.com",
        "www.cell.com", "www.thelancet.com", "www.nejm.org",
    ],
    "enterprise_saas": [
        "github.com", "gitlab.com", "www.atlassian.com", "www.salesforce.com", "slack.com", "www.notion.so",
        "www.zoom.us", "www.dropbox.com", "www.box.com", "www.zendesk.com",
    ],
    "developer_platforms": [
        "www.npmjs.com", "pypi.org", "crates.io", "packagist.org", "hub.docker.com",
        "bitbucket.org", "vercel.com", "www.heroku.com", "render.com", "fly.io",
    ],
}

WIKI_TOPICS = [
    "Web_scraping", "World_Wide_Web", "Graph_theory", "Semantic_Web", "Ontology",
    "Machine_learning", "Distributed_computing", "Workflow", "Memory", "Runtime_system",
]

PATHS = [
    "", "/about", "/news", "/blog", "/docs", "/api", "/products", "/contact",
    "/help", "/support", "/pricing", "/features", "/learn", "/guides",
]


def build_matrix() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()

    for category, hosts in HOSTS.items():
        for host in hosts:
            if category == "wikipedia":
                for topic in WIKI_TOPICS:
                    url = f"https://{host}/wiki/{topic}"
                    if url not in seen:
                        seen.add(url)
                        rows.append({"category": category, "url": url})
                continue
            for path in PATHS:
                url = f"https://{host}{path}"
                if url in seen:
                    continue
                seen.add(url)
                rows.append({"category": category, "url": url})
                if len(rows) >= 1200:
                    return rows
    return rows


def main() -> int:
    matrix = build_matrix()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"version": 1, "count": len(matrix), "urls": matrix}, indent=2), encoding="utf-8")
    print(f"Wrote {len(matrix)} URLs -> {OUT}")
    return 0 if len(matrix) >= 1000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
