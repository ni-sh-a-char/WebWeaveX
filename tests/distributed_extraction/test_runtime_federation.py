from core.distributed_extraction import federate_extraction_runtimes
from core.distributed_extraction.distributed_adaptive_runtime_engine import (
    synchronize_adaptive_runtime,
)
from core.distributed_extraction.distributed_stream_engine import (
    federate_stream_runtimes,
)


def test_stream_federation():
    streams = [
        {
            "worker_id": "w0",
            "events": [
                {
                    "id": "stream_0",
                    "timestamp": 0,
                    "source": "websocket",
                    "direction": "incoming",
                    "payload": "a",
                    "connection_id": "ws",
                    "bounded": True,
                }
            ],
        },
        {
            "worker_id": "w1",
            "events": [
                {
                    "id": "stream_1",
                    "timestamp": 1,
                    "source": "sse",
                    "direction": "incoming",
                    "payload": "b",
                    "connection_id": "sse",
                    "bounded": True,
                }
            ],
        },
    ]

    merged = federate_stream_runtimes(streams)

    assert len(merged["events"]) == 2
    assert merged["events"][0]["payload"] == "a"


def test_adaptive_sharing():
    states = [
        {"memory": {"healed_selectors": {"#a": "button"}}},
        {"memory": {"healed_selectors": {"#b": "[aria-label='next']"}}},
    ]

    synced = synchronize_adaptive_runtime(states)

    assert "#a" in synced["healed_selectors"]
    assert "#b" in synced["healed_selectors"]


def test_runtime_federation_graph():
    runtimes = [
        {
            "ir": "browser",
            "nodes": [{"id": "n1", "type": "page"}],
            "edges": [],
        }
    ]

    result = federate_extraction_runtimes(runtimes)

    assert result["topology"]["nodes"]
