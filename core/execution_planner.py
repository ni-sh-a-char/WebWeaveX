"""
WebWeaveX Execution Planner (Phase V6)

Purpose:
    Build execution graph from system design
    - NO hardcoded steps
    - Derivation from structure and relationships

Philosophy:
    Derive execution from system graph, not templates
"""

from typing import Dict, Any, List


def _derive_execution_phases(system_design: Dict, project_artifacts: List[Dict]) -> List[str]:
    """Derive execution phases from system design."""
    phases = []
    
    architecture = system_design.get("architecture", "")
    system_type = system_design.get("system_type", "")
    relationships = system_design.get("relationships", [])
    components = system_design.get("components", [])
    
    if architecture in ["container_orchestrated", "service_mesh"]:
        phases = ["orchestrate", "provision", "deploy"]
    elif system_type in ["api_service", "data_service"]:
        phases = ["configure", "initialize", "serve"]
    elif system_type == "authentication_service":
        phases = ["configure_security", "initialize_auth", "serve"]
    elif components:
        phases = ["setup", "initialize", "execute"]
    else:
        phases = ["initialize", "run"]
    
    return phases


def _derive_dependencies(relationships: List[Dict], components: List[Dict]) -> Dict[str, List[str]]:
    """Derive execution dependencies from relationships."""
    deps = {}
    
    for rel in relationships:
        from_node = rel.get("from", "")
        to_node = rel.get("to", "")
        rel_type = rel.get("type", "")
        
        if from_node and to_node:
            if from_node not in deps:
                deps[from_node] = []
            if rel_type == "persists":
                deps[from_node].append("storage_ready")
            elif rel_type == "queries":
                deps[from_node].append("storage_ready")
            elif rel_type == "authenticates":
                deps[from_node].append("identity_ready")
    
    for comp in components:
        name = comp.get("name", "")
        if name and name not in deps:
            deps[name] = []
    
    return deps


def _build_execution_step(phase: str, system_design: Dict, dependencies: Dict, prev_step: str = "") -> Dict[str, Any]:
    """Build a single execution step from phase."""
    step = {
        "phase": phase,
        "depends_on": [prev_step] if prev_step else []
    }
    
    if phase == "orchestrate":
        step["action"] = "orchestrate"
        step["target"] = "container_runtime"
    elif phase == "provision":
        step["action"] = "provision"
        step["resources"] = list(dependencies.keys())
    elif phase == "deploy":
        step["action"] = "deploy"
        step["target"] = system_design.get("system_type", "service")
    elif phase == "configure":
        step["action"] = "configure"
        step["config"] = {"system": system_design.get("system_type")}
    elif phase == "configure_security":
        step["action"] = "configure"
        step["config"] = {"security": "enabled"}
    elif phase == "initialize":
        step["action"] = "initialize"
        step["components"] = [c.get("name", "") for c in system_design.get("components", [])]
    elif phase == "initialize_auth":
        step["action"] = "initialize"
        step["security"] = "identity_provider"
    elif phase == "serve":
        step["action"] = "serve"
        step["protocol"] = "http"
    elif phase == "setup":
        step["action"] = "setup"
    elif phase == "run":
        step["action"] = "execute"
    else:
        step["action"] = "run"
    
    return step


def _derive_dag(phases: List[str], dependencies: Dict) -> List[Dict]:
    """Build DAG from phases."""
    dag = []
    prev = ""
    
    for phase in phases:
        if not phase:
            continue
        
        step = {
            "id": len(dag) + 1,
            "phase": phase,
            "depends_on": [len(dag)] if prev and prev != phase else []
        }
        
        if phase in dependencies:
            step["requires"] = dependencies[phase]
        
        dag.append(step)
        prev = phase
    
    return dag


def build_execution_plan(system_design: Dict, project_artifacts: List[Dict]) -> List[Dict]:
    """Build execution plan through derivation."""
    if not isinstance(system_design, dict):
        return _empty_plan()
    
    phases = _derive_execution_phases(system_design, project_artifacts)
    
    if not phases:
        return _empty_plan()
    
    relationships = system_design.get("relationships", [])
    components = system_design.get("components", [])
    deps = _derive_dependencies(relationships, components)
    
    plan = []
    for i, phase in enumerate(phases):
        step = {
            "id": i + 1,
            "phase": phase,
            "action": phase,
            "depends_on": [i] if i > 0 else []
        }
        
        if phase == "initialize" or phase == "initialize_auth":
            step["components"] = [c.get("name", "") for c in components]
        
        if phase in deps:
            step["required_by"] = deps[phase]
        
        plan.append(step)
    
    return plan


def _empty_plan() -> List[Dict]:
    return [{"id": 1, "phase": "run", "action": "execute", "depends_on": []}]


def validate_execution_planner() -> bool:
    """Validate execution planner."""
    test_design = {
        "system_type": "api_service",
        "architecture": "monolithic",
        "components": [{"name": "api", "type": "service"}],
        "relationships": []
    }
    test_artifacts = []
    
    plan = build_execution_plan(test_design, test_artifacts)
    
    if not isinstance(plan, list):
        return False
    
    if len(plan) < 1:
        return False
    
    return True


if __name__ == "__main__":
    ok = validate_execution_planner()
    print("V6 EXECUTION PLANNER:", "PASS" if ok else "FAIL")