from core.ir.repository_runtime_ir import compile_repository_runtime_ir


def test_compile_repository_runtime_ir():
    result = compile_repository_runtime_ir(
        ingestion={"file_count": 1},
        languages={"primary_language": "python"},
        graph={"nodes": [], "edges": []},
        services={"services": []},
        infra={"infra": []},
        topology={"nodes": [], "edges": []},
        dependencies={"imports": ["os"], "edges": []},
        apis={"routes": ["/health"], "per_file": []},
        execution_flows={"flows": []},
    )

    assert result["ir"] == "repository_runtime"
    assert result["dependencies"] == ["os"]
    assert result["apis"] == ["/health"]
    assert result["bounded"] is True
