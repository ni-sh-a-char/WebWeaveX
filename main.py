from core.crawler import WebCrawler
from core.learning_pipeline import run_learning
from core.memory_context import MemoryContext


if __name__ == "__main__":
    crawler = WebCrawler()
    url = input("Enter URL: ")
    context = MemoryContext()
    results = crawler.crawl(url, depth=2, goal="extract knowledge", use_multi_agent=True, context=context)
    run_learning(context)
    print(results)
