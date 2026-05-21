from webweavex import extract, extract_async, extract_repo, extract_docs, analyze, fingerprint
from core.schemas.validator import validate_contract
import asyncio


def run_validation():
    base = extract('local deterministic source')
    llm = extract({'source':'local deterministic source','llm':'groq'})
    graph = base.get('relationships', {}).get('execution_graph', {})
    async_out = asyncio.run(extract_async('x'))
    return {
        'deterministic_outputs': extract('x') == extract('x'),
        'graph_stability': graph.get('max_edges') == 500,
        'schema_stability': validate_contract(base, 'extraction.schema.json'),
        'fingerprint_parity': fingerprint(base) == fingerprint(base),
        'no_type_fields': all(set(e.keys()) == {'from','to'} for e in graph.get('edges', [])),
        'bounded_graphs': len(graph.get('edges', [])) <= 500,
        'llm_isolation': base['fingerprint'] == llm['fingerprint'],
        'async_correctness': isinstance(async_out, dict),
        'security_correctness': extract('http://127.0.0.1/x')['metadata']['fetch']['ok'] is False,
        'repository_intelligence_correctness': 'repository_intelligence_v12' in base.get('content', {}),
        'document_intelligence_correctness': 'document_intelligence_v12' in base.get('content', {}),
        'api_ergonomics': isinstance(extract_repo('x'), dict) and isinstance(extract_docs('x'), dict) and isinstance(analyze('x'), dict),
    }

if __name__ == '__main__':
    print(run_validation())
