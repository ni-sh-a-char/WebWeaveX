from core.ipc import SemanticIPC
from core.process import SemanticProcess, SemanticProcessTable


def test_ipc_send_receive():
    bus = SemanticIPC()
    bus.send({"pid": 1, "msg": "hello"})
    msg = bus.receive()
    assert msg.get("msg") == "hello"


def test_process_table_snapshot():
    table = SemanticProcessTable()
    table.register(SemanticProcess(pid=1, state="running", memory={}, tasks=[]))
    snap = table.snapshot()
    assert snap["count"] == 1
    assert snap["pids"] == [1]
