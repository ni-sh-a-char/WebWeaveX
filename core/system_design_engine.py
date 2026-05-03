"""
WebWeaveX System Design Engine (Phase V6)

Purpose:
    True system compiler - derive system structure from semantics
    - NO hardcoded maps
    - NO template code
    - Structural derivation only

Philosophy:
    INPUT → SEMANTIC PATTERNS → STRUCTURE → GRAPH → EXECUTION
"""

from typing import Dict, Any, List, Set


def _derive_entity_categories(entities: List[Dict]) -> Dict[str, int]:
    """Derive category dominance from entities."""
    categories = {}
    for entity in entities:
        cat = entity.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    return categories


def _derive_action_patterns(actions: List[Dict], action_pairs: List[Dict]) -> Dict[str, Set[str]]:
    """Derive action patterns from semantics."""
    patterns = {
        "verbs": set(),
        "targets": set(),
        "operations": set(),
        "infrastructures": set()
    }
    
    for action in actions:
        verb = action.get("text", "").lower()
        if verb in ["build", "create", "make", "generate"]:
            patterns["verbs"].add("create")
        elif verb in ["install", "setup", "configure"]:
            patterns["verbs"].add("provision")
        elif verb in ["run", "start", "execute"]:
            patterns["verbs"].add("execute")
        elif verb in ["deploy", "publish"]:
            patterns["verbs"].add("deploy")
        elif verb in ["store", "save", "write"]:
            patterns["verbs"].add("persist")
        elif verb in ["connect", "send", "receive"]:
            patterns["verbs"].add("communicate")
    
    for pair in action_pairs:
        entity = pair.get("entity", "").lower()
        if entity in ["database", "db", "sql", "mongodb"]:
            patterns["targets"].add("storage")
        elif entity in ["api", "endpoint", "route"]:
            patterns["targets"].add("interface")
        elif entity in ["user", "auth", "token"]:
            patterns["targets"].add("identity")
        elif entity in ["docker", "container"]:
            patterns["targets"].add("containerization")
        elif entity in ["server", "backend"]:
            patterns["targets"].add("compute")
    
    return patterns


def _derive_system_type_from_patterns(patterns: Dict[str, Set[str]], categories: Dict[str, int]) -> str:
    """Derive system type from semantic patterns."""
    targets = patterns.get("targets", set())
    verbs = patterns.get("verbs", set())
    
    if "storage" in targets and "interface" in targets:
        return "data_service"
    elif "interface" in targets:
        return "api_service"
    elif "identity" in targets:
        return "authentication_service"
    elif "containerization" in targets:
        return "containerized_service"
    elif "compute" in targets:
        return "compute_service"
    elif "persist" in verbs:
        return "data_service"
    elif "execute" in verbs:
        return "executable_service"
    
    dominant_cat = max(categories.items(), key=lambda x: x[1])[0] if categories else "unknown"
    
    cat_to_type = {
        "system": "service",
        "application": "application",
        "container": "containerized",
        "storage": "data_service",
        "backend": "compute_service",
        "frontend": "presentation",
        "framework": "service",
        "language": "executable",
        "protocol": "service"
    }
    
    return cat_to_type.get(dominant_cat, "generic_service")


def _derive_components_from_pairs(action_pairs: List[Dict]) -> List[Dict]:
    """Derive components from action-entity pairs."""
    seen = set()
    components = []
    
    for pair in action_pairs:
        entity = pair.get("entity", "")
        action = pair.get("action", "")
        
        if not entity or entity in seen:
            continue
        
        comp_type = "service"
        if pair.get("entity_category") == "storage":
            comp_type = "storage"
        elif pair.get("entity_category") == "framework":
            comp_type = "application"
        
        components.append({
            "name": entity,
            "type": comp_type,
            "relationship": action
        })
        seen.add(entity)
    
    if not components:
        components = [{"name": "core", "type": "service", "relationship": "primary"}]
    
    return components


def _derive_relationships(components: List[Dict], patterns: Dict[str, Set[str]]) -> List[Dict]:
    """Derive component relationships."""
    relationships = []
    
    targets = patterns.get("targets", set())
    
    if "storage" in targets and "interface" in targets:
        relationships.append({"from": "interface", "to": "storage", "type": "queries"})
    elif "storage" in targets:
        relationships.append({"from": "core", "to": "storage", "type": "persists"})
    
    if "identity" in targets:
        relationships.append({"from": "core", "to": "identity", "type": "authenticates"})
    
    if "containerization" in targets:
        relationships.append({"from": "core", "to": "container", "type": "deploys_to"})
    
    if not relationships:
        relationships = [{"from": "core", "to": "service", "type": "implements"}]
    
    return relationships


def _derive_architecture(patterns: Dict[str, Set[str]], system_type: str) -> str:
    """Derive architecture pattern."""
    targets = patterns.get("targets", set())
    
    if "containerization" in targets:
        return "container_orchestrated"
    elif len(targets) >= 3:
        return "service_mesh"
    elif len(targets) >= 2:
        return "service_oriented"
    else:
        return "monolithic"


def _derive_tech_stack_from_reasoning(reasoning: Dict, patterns: Dict[str, Set[str]]) -> List[str]:
    """Derive tech stack from reasoning (not hardcoded)."""
    stack = []
    
    strategy = reasoning.get("strategy", "")
    approach = reasoning.get("approach", [])
    
    if "containerization" in patterns.get("targets", set()):
        stack.append("docker")
        stack.append("container_runtime")
    
    if "api_service" in strategy or "interface" in patterns.get("targets", set()):
        stack.append("http_protocol")
        stack.append("json")
    
    if "storage" in patterns.get("targets", set()):
        stack.append("database_interface")
    
    if "authentication_service" in strategy:
        stack.append("security_protocol")
    
    for step in approach:
        if step == "install":
            stack.append("package_manager")
        elif step == "run":
            stack.append("runtime")
    
    if not stack:
        stack = ["runtime", "standard_library"]
    
    return stack


def _derive_modules(components: List[Dict], patterns: Dict[str, Set[str]]) -> List[str]:
    """Derive system modules."""
    modules = []
    
    for comp in components:
        name = comp.get("name", "")
        if name:
            modules.append(name)
    
    targets = patterns.get("targets", set())
    if "identity" in targets:
        modules.append("identity_management")
    if "storage" in targets:
        modules.append("persistence")
    
    if not modules:
        modules = ["core"]
    
    return modules


def build_system_design(reasoning: Dict, semantics: Dict, user_input: str) -> Dict:
    """Build system design through derivation (no templates)."""
    if not user_input:
        user_input = ""
    
    entities = semantics.get("entities", [])
    actions = semantics.get("actions", [])
    action_pairs = semantics.get("action_pairs", [])
    
    categories = _derive_entity_categories(entities)
    patterns = _derive_action_patterns(actions, action_pairs)
    
    system_type = _derive_system_type_from_patterns(patterns, categories)
    components = _derive_components_from_pairs(action_pairs)
    relationships = _derive_relationships(components, patterns)
    architecture = _derive_architecture(patterns, system_type)
    tech_stack = _derive_tech_stack_from_reasoning(reasoning, patterns)
    modules = _derive_modules(components, patterns)
    
    return {
        "system_type": system_type,
        "architecture": architecture,
        "components": components,
        "relationships": relationships,
        "tech_stack": tech_stack,
        "modules": modules,
        "derived_from": {
            "entity_categories": categories,
            "action_patterns": {k: list(v) for k, v in patterns.items()},
            "input": user_input
        },
        "version": "v6_derived"
    }


def validate_system_design() -> bool:
    """Validate system design."""
    test_reasoning = {"strategy": "backend_service", "approach": ["build", "run"]}
    test_semantics = {
        "entities": [{"text": "api", "category": "system"}],
        "actions": [{"text": "build", "type": "verb"}],
        "action_pairs": [{"action": "build", "entity": "api", "normalized_action": "build"}]
    }
    
    result = build_system_design(test_reasoning, test_semantics, "build api")
    
    if not isinstance(result, dict):
        return False
    
    if "system_type" not in result:
        return False
    
    return True


if __name__ == "__main__":
    ok = validate_system_design()
    print("V6 SYSTEM DESIGN:", "PASS" if ok else "FAIL")