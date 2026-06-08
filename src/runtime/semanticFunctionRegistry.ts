/**
 * Converted from Python: core/runtime/semantic_function_registry.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export class SemanticFunctionRegistry {
  declare _functions: any;
  constructor() {
    this._functions = {};
  }
  register(name: any, fn: any): any {
    py.setItem(this._functions, name, fn);
  }
  call(name: any, ...args: any[]): any {
    var kwargs: Record<string, any> = {};
    return py.at(this._functions, name)(...py.iter(args), kwargs);
  }
}
