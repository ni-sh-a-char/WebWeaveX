/**
 * Converted from Python: core/transactions/semantic_transaction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticTransaction {
  declare operations: any;
  declare committed: any;
  constructor() {
    this.operations = [];
    this.committed = false;
  }
  add_operation(operation: any): any {
    if (py.truthy(this.committed)) {
      return;
    }
    py.listAppend(this.operations, operation);
  }
  commit(): any {
    this.committed = true;
    return {"operations": py.len(this.operations), "committed": true};
  }
  rollback(): any {
    var count: any = py.len(this.operations);
    py.clear(this.operations);
    return {"rolled_back": count};
  }
}
