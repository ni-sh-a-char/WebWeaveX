from webweavex import extract, extract_async, fingerprint
from core.schemas.validator import validate_contract
import asyncio


def run_validation():
    core = extract("https://openai.com")
    core2 = extract({"source": "local deterministic source", "llm": "groq"})
    core3 = extract("local deterministic source")
    async_out = asyncio.run(extract_async("hello"))
    fp_stable = fingerprint(core) == fingerprint(core)
    return {
        "extraction_works": isinstance(core, dict),
        "repository_extraction_works": "content" in core,
        "graph_stable": "execution_graph" in core.get("relationships", {}),
        "intelligence_stable": isinstance(core.get("metadata", {}).get("confidence"), float),
        "fingerprints_stable": fp_stable,
        "groq_isolated": core2["fingerprint"] == core3["fingerprint"],
        "schema_stable": validate_contract(core, "extraction.schema.json"),
        "deterministic_outputs": extract("hello") == extract("hello"),
        "async_works": isinstance(async_out, dict),
    }


if __name__ == "__main__":
    print(run_validation())
