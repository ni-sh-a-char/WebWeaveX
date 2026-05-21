from __future__ import annotations

from typing import Any, Dict

from core.compiler.semantic_lowering_engine import lower_semantic_ir
from core.compiler.semantic_optimization_pipeline import optimize_semantic_pipeline
from core.compiler.semantic_execution_planner import build_semantic_execution_plan
from core.compiler.semantic_bytecode_optimizer import optimize_semantic_bytecode
from core.bytecode import compile_semantic_bytecode


def compile_semantic_pipeline(ir: Dict[str, Any]) -> Dict[str, Any]:
    lowered = lower_semantic_ir(ir)

    optimized = optimize_semantic_pipeline(lowered)

    execution_plan = build_semantic_execution_plan(optimized)

    bytecode_edges = {
        "edges": [
            {"from": e.get("source"), "to": e.get("target")}
            for e in optimized.get("optimized_edges", [])
        ]
    }
    bytecode = compile_semantic_bytecode(bytecode_edges)
    instruction_dicts = [
        {"opcode": ins.opcode, "operand": ins.operand}
        for ins in bytecode.get("instructions", [])
    ]
    bytecode_optimized = optimize_semantic_bytecode(instruction_dicts)

    return {
        "lowered_ir": lowered,
        "optimized_ir": optimized,
        "execution_plan": execution_plan,
        "bytecode": bytecode,
        "bytecode_optimized": bytecode_optimized,
    }
