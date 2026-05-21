from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.unified_runtime_ir import compile_unified_runtime_ir, unified_runtime_ir_to_graph
from core.kernel.runtime_boundary import enforce_runtime_boundary
from core.kernel.runtime_bus import publish_runtime_event
from core.kernel.runtime_coordination import coordinate_kernel_phases
from core.kernel.runtime_dispatcher import dispatch_runtime_phase
from core.kernel.runtime_execution_bridge import run_execution_phase
from core.kernel.runtime_graph_bridge import merge_runtime_graph
from core.kernel.runtime_lifecycle import initialize_runtime, shutdown_runtime
from core.kernel.runtime_memory_bridge import run_memory_phase
from core.kernel.runtime_policy import build_kernel_policy, enforce_kernel_policy
from core.kernel.runtime_registry import list_runtime_phases, register_runtime_phase
from core.kernel.runtime_replay import replay_kernel_state
from core.kernel.runtime_scheduler import schedule_kernel_phases
from core.kernel.runtime_semantic_bridge import run_semantic_phase
from core.kernel.runtime_state import build_kernel_state, merge_kernel_state
from core.kernel.runtime_sync_bridge import run_sync_phase
from core.kernel.runtime_topology import build_kernel_topology
from core.reconstruction.runtime_reconstruction_orchestrator import run_reconstruction_for_extraction


class RuntimeKernel:
    """Single canonical operational substrate routing all runtime phases."""

    def __init__(self, runtime_type: str = "browser") -> None:
        self.runtime_type = runtime_type
        self._initialized = initialize_runtime(runtime_type=runtime_type)
        self._bus: List[Dict[str, Any]] = []
        self._registry: Dict[str, Any] = {"phases": {}}
        self._irs: List[Dict[str, Any]] = []

    def run_pipeline(
        self,
        sources: Optional[Dict[str, Any]] = None,
        tick: int = 0,
        phases: Optional[List[str]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        sources = sources or {}
        options = options or {}
        active_phases = phases or [
            "semantic",
            "synchronization",
            "memory",
            "execution",
            "reconstruction",
        ]
        schedule = schedule_kernel_phases(active_phases, tick=tick)
        policy = build_kernel_policy()
        phase_results: List[Dict[str, Any]] = []
        state = dict(self._initialized.get("state", {}))

        for entry in schedule["scheduled"]:
            phase = entry["phase"]
            if phase == "semantic" and options.get("semantic", True):
                result = dispatch_runtime_phase(
                    phase,
                    lambda **kw: run_semantic_phase(sources=sources, tick=tick, **options.get("semantic_opts", {})),
                    state.get("context", {}),
                )
            elif phase == "synchronization" and options.get("sync", True):
                result = dispatch_runtime_phase(
                    phase,
                    lambda **kw: run_sync_phase(sources=sources, tick=tick, **options.get("sync_opts", {})),
                    state.get("context", {}),
                )
            elif phase == "memory" and options.get("memory", True):
                result = dispatch_runtime_phase(
                    phase,
                    lambda **kw: run_memory_phase(sources=sources, tick=tick, **options.get("memory_opts", {})),
                    state.get("context", {}),
                )
            elif phase == "execution" and options.get("execution", True):
                result = dispatch_runtime_phase(
                    phase,
                    lambda **kw: run_execution_phase(
                        sources=sources,
                        runtime=self.runtime_type,
                        tick=tick,
                        **options.get("execution_opts", {}),
                    ),
                    state.get("context", {}),
                )
            elif phase == "reconstruction" and options.get("reconstruction", True):
                result = dispatch_runtime_phase(
                    phase,
                    lambda **kw: run_reconstruction_for_extraction(
                        reconstruction_runtime=True,
                        sources=sources,
                        runtime_type=self.runtime_type,
                        tick=tick,
                        merge_graph=False,
                        **options.get("reconstruction_opts", {}),
                    ),
                    state.get("context", {}),
                )
            else:
                continue

            phase_results.append(result)
            self._registry = register_runtime_phase(
                self._registry,
                phase,
                result.get("result", {}),
            )
            bus_update = publish_runtime_event(self._bus, phase, result, tick=tick)
            self._bus = bus_update["bus"]

            ir_key = f"{phase}_ir"
            ir_payload = result.get("result", {}).get(ir_key, result.get("result", {}).get("memory_ir"))
            if ir_payload:
                self._irs.append(ir_payload)

        graph = merge_runtime_graph(self._irs) if self._irs else {}
        topology = build_kernel_topology(graph)
        enforcement = enforce_kernel_policy(
            policy,
            len(phase_results),
            topology.get("node_count", 0),
        )
        boundary = enforce_runtime_boundary({"irs": self._irs, "graph": graph})

        unified_ir = compile_unified_runtime_ir(
            registry=self._registry,
            graph=graph,
            bus=self._bus,
            phase_results=phase_results,
        )
        coordination = coordinate_kernel_phases(phase_results, tick=tick)
        replay = replay_kernel_state(self._bus)

        payload = {
            "runtime_type": self.runtime_type,
            "schedule": schedule,
            "registry": self._registry,
            "coordination": coordination,
            "topology": topology,
            "graph": graph,
            "unified_ir": unified_ir,
            "replay": replay,
            "policy_enforcement": enforcement,
            "boundary": boundary,
            "phases": list_runtime_phases(),
            "bounded": True,
        }
        state = merge_kernel_state(state, {"graph": graph, "irs": self._irs})
        payload["state"] = state
        return payload

    def shutdown(self) -> Dict[str, Any]:
        return shutdown_runtime(self._initialized.get("state", {}))


_KERNEL: Optional[RuntimeKernel] = None


def get_runtime_kernel(runtime_type: str = "browser") -> RuntimeKernel:
    global _KERNEL
    if _KERNEL is None or _KERNEL.runtime_type != runtime_type:
        _KERNEL = RuntimeKernel(runtime_type=runtime_type)
    return _KERNEL
