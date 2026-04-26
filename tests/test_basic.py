from core.crawler import WebCrawler

crawler = WebCrawler()
result = crawler.crawl("https://example.com", depth=1)
print(result)