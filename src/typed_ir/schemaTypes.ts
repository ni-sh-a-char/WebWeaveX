/**
 * Converted from Python: core/typed_ir/schema_types.py
 * @generated — WebWeaveX python→javascript library port
 */


export class SemanticNode {
  declare id: any;
  declare type: any;
  declare attributes: any;
  constructor(id: any, type: any, attributes: any = {}) {
    this.id = id;
    this.type = type;
    this.attributes = attributes;
  }
}
export class SemanticEdge {
  declare source: any;
  declare target: any;
  declare relation: any;
  declare evidence: any;
  constructor(source: any, target: any, relation: any, evidence: any = []) {
    this.source = source;
    this.target = target;
    this.relation = relation;
    this.evidence = evidence;
  }
}
export class ExecutionState {
  declare id: any;
  declare state_type: any;
  declare variables: any;
  constructor(id: any, state_type: any, variables: any = {}) {
    this.id = id;
    this.state_type = state_type;
    this.variables = variables;
  }
}
export class RuntimeTransition {
  declare from_state: any;
  declare to_state: any;
  declare transition_type: any;
  constructor(from_state: any, to_state: any, transition_type: any) {
    this.from_state = from_state;
    this.to_state = to_state;
    this.transition_type = transition_type;
  }
}
