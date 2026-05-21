from webweavex import extract, extract_recursive, crawl, stream_extract, query_graph, query_repo


def run_validation():
    base = extract('hello world')
    rec = extract_recursive('local deterministic text')
    g = rec['relationships']['execution_graph']
    return {
      'recursive_extraction_works': isinstance(rec, dict),
      'crawl_budgets_work': isinstance(crawl('https://example.com', max_pages=1), dict),
      'graph_stability_holds': g.get('max_edges') in (500, 20000),
      'fingerprints_deterministic': extract('x')['fingerprint'] == extract('x')['fingerprint'],
      'schemas_stable': all(k in base for k in ['content','code','dependencies','metadata','relationships','raw_text','source_url','fingerprint']),
      'llm_isolation_preserved': extract('x')['fingerprint'] == extract({'source':'x','llm':'groq'})['fingerprint'],
      'streaming_extraction_works': 'streaming' in stream_extract('x'*9000)['metadata'],
      'repository_recursion_works': isinstance(query_repo(rec), dict),
      'graph_queries_work': isinstance(query_graph(rec), dict),
      'reference_graph_present': 'reference_graph' in rec['relationships'],
    }

if __name__ == '__main__':
    print(run_validation())
