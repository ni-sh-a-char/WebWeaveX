/**
 * Converted from Python: core/actors/semantic_actor_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ACTORS: any = 1000;
export let MAX_MAILBOX: any = 10000;
export class SemanticActor {
  declare actor_id: any;
  declare mailbox: any;
  constructor(actor_id: any, mailbox: any) {
    this.actor_id = actor_id;
    this.mailbox = mailbox;
  }
}
export class SemanticActorSystem {
  declare actors: any;
  constructor() {
    this.actors = {};
  }
  create_actor(actor_id: any): any {
    if ((py.len(this.actors) >= MAX_ACTORS)) {
      return;
    }
    py.setItem(this.actors, actor_id, new SemanticActor(actor_id, py.deque([])));
  }
  send(actor_id: any, message: any): any {
    var actor: any = py.get(this.actors, actor_id);
    if ((actor === null || actor === undefined)) {
      return;
    }
    if ((py.len(actor.mailbox) >= MAX_MAILBOX)) {
      return;
    }
    py.listAppend(actor.mailbox, message);
  }
  receive(actor_id: any): any {
    var actor: any = py.get(this.actors, actor_id);
    if ((actor === null || actor === undefined)) {
      return {"missing": true};
    }
    if (!py.truthy(actor.mailbox)) {
      return {"empty": true};
    }
    return py.popleft(actor.mailbox);
  }
}
