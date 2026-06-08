/**
 * Converted from Python: core/transactions/distributed_transaction_coordinator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function coordinateTransactions(transactions: any): any {
  var committed: any[] = [];
  var tx: any;
  for (tx of py.iter(transactions)) {
    py.listAppend(committed, {"id": py.get(tx, "id"), "committed": true});
  }
  return {"transactions": committed};
}
