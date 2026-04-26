import sys
sys.path.insert(0, '.')

from core.plugins import PLUGINS, register_plugin
from core.crawler import WebCrawler

def my_plugin(data):
    return data + "_MODIFIED"

register_plugin("pre_extract", my_plugin)

print("Pre plugins count:", len(PLUGINS['pre_extract']))

crawler = WebCrawler()
r = crawler.crawl("https://example.com", depth=1)
print("Crawl successful:", r[0]["url"])