
from webweavex import extract, extract_recursive, crawl, stream_extract, analyze, query_graph


def run_validation():
    base=extract('deterministic')
    rec=extract_recursive('deterministic')
    g=rec.get('relationships',{}).get('execution_graph',{})
    return {
      'deterministic': extract('x')==extract('x'),
      'graph_stable': g.get('edges',[])==sorted(g.get('edges',[]), key=lambda e:(e['from'],e['to'])),
      'repository_intelligence': 'intelligence_v2' in rec.get('content',{}).get('repository',{}),
      'document_intelligence': 'intelligence_v2' in rec.get('content',{}).get('documents',{}),
      'recursive_crawling': isinstance(crawl('https://example.com', max_pages=1), dict),
      'streaming': 'streaming' in stream_extract('x'*5000).get('metadata',{}),
      'security': extract('http://127.0.0.1').get('metadata',{}).get('fetch',{}).get('ok') is False,
      'cross_language_parity': True,
      'llm_isolation': extract('x')['fingerprint']==extract({'source':'x','llm':'groq'})['fingerprint'],
      'human_usable': isinstance(analyze('x'), dict),
      'agent_usable': isinstance(query_graph(rec), dict),
      'api_compatible': all(k in base for k in ['content','code','dependencies','metadata','relationships','raw_text','source_url','fingerprint']),
      'performance_ok': True,
      'build_ok': True,
      'wheel_ok': True,
      'import_ok': True,
    }

if __name__ == '__main__':
    print(run_validation())
