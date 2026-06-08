const MAX_VM_STEPS = 10_000;

export type SemanticInstruction = {
  opcode: string;
  operand?: Record<string, unknown>;
};

export class SemanticVirtualMachine {
  memory: Record<string, unknown> = {};
  executionLog: Array<Record<string, unknown>> = [];

  execute(instructions: SemanticInstruction[]): Record<string, unknown> {
    let executed = 0;
    for (const ins of instructions) {
      if (executed >= MAX_VM_STEPS) break;
      if (ins.opcode === "LINK" && ins.operand) {
        const key = `${ins.operand.from}->${ins.operand.to}`;
        this.memory[key] = true;
      }
      this.executionLog.push({ opcode: ins.opcode });
      executed += 1;
    }
    return { executed, memory: this.memory, bounded: true };
  }
}

export function runSemanticVm(instructions: SemanticInstruction[]): Record<string, unknown> {
  return new SemanticVirtualMachine().execute(instructions);
}
