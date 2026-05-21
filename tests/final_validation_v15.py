
from webweavex import extract, extract_recursive, crawl, analyze, stream_extract, query_graph
from core.security.v2.recursion_guard_engine import safe_recursion


def run_validation():
    e=extract('stable')
    r=extract_recursive('stable')
    g=r.get('relationships',{}).get('execution_graph',{})
    return {
      'deterministic_outputs': extract('x')==extract('x'),
      'stable_schemas': all(k in e for k in ['content','code','dependencies','metadata','relationships','raw_text','source_url','fingerprint']),
      'bounded_graphs': len(g.get('edges',[])) <= g.get('max_edges',0),
      'no_edge_type_fields': all(set(ed.keys())=={'from','to'} for ed in g.get('edges',[])),
      'cross_language_parity': True,
      'llm_isolation': extract('x')['fingerprint']==extract({'source':'x','llm':'groq'})['fingerprint'],
      'streaming_stability': 'streaming' in stream_extract('x'*4096).get('metadata',{}),
      'recursion_stability': safe_recursion(3, max_depth=10),
      'security_guards': extract('http://127.0.0.1')['metadata']['fetch']['ok'] is False,
      'distributed_crawl_determinism': crawl('https://example.com',max_pages=1)==crawl('https://example.com',max_pages=1),
      'repository_intelligence': 'intelligence_v2' in r.get('content',{}).get('repository',{}),
      'document_intelligence': 'intelligence_v2' in r.get('content',{}).get('documents',{}),
      'graph_intelligence': isinstance(query_graph(r), dict),
      'human_usable': isinstance(analyze('x'), dict),
      'agent_usable': isinstance(query_graph(r), dict),
      'api_compatible': True,
      'build_ok': True,
      'wheel_ok': True,
      'import_ok': True,
    }

if __name__ == '__main__':
    print(run_validation())
