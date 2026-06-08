/**
 * Converted from Python: core/agents/semantic_agent_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { SemanticAgent } from "./semanticAgentEngine.js";

export class SemanticAgentRuntime {
  declare _agents: any;
  constructor() {
    this._agents = {};
  }
  register(agent: any): any {
    py.setItem(this._agents, agent.agent_id, agent);
  }
  execute(agent_id: any, task: any): any {
    var agent: any = py.at(this._agents, agent_id);
    return agent.execute(task);
  }
}
export { SemanticAgent };
