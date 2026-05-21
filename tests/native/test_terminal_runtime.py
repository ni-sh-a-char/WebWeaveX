from core.native.native_terminal_engine import capture_terminal_runtime
from core.native.native_replay_engine import replay_native_runtime
from core.native.native_memory_engine import remember_native_runtime


def test_terminal_replay():
    terminal = capture_terminal_runtime(
        snapshot={
            "output": ["$ ls", "file.txt"],
            "commands": ["ls"],
            "prompts": ["$"],
            "stream_id": "terminal:1",
        },
    )

    memory = remember_native_runtime({}, {"terminal_streams": terminal})
    first = replay_native_runtime(memory)
    second = replay_native_runtime(memory)

    assert first == second
    assert first["terminal_flows"]["replay_token"] == terminal["replay_token"]
