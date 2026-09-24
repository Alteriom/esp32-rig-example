"""Three tests, one row per board: the firmware boots and says what it is,
its serial path is clean, and it does the one thing it is for."""

import pytest

# Compile-only CI cannot exercise any of these; the rig can. In sim mode
# they still run, against the simulator, as a check on the suite itself.
pytestmark = pytest.mark.hil_only(reason="real silicon")


@pytest.mark.capability("example.boot")
def test_the_board_boots_and_says_what_it_is(board, board_id):
    info = board.ensure_responsive()
    assert info.get("bootId"), f"{board_id} answered info with no boot id"
    assert info.get("family"), f"{board_id} did not say which family it was built for"


@pytest.mark.capability("example.serial")
def test_the_serial_path_returns_a_line_byte_for_byte(board, board_id):
    text = "the quick brown fox jumps over the lazy dog " * 8
    reply = board.send_cmd_awaiting("echo", lambda e: e["evt"] == "echo", "echo reply", timeout=5, text=text)
    assert reply.get("text") == text, f"{board_id} returned a different line than it was sent"


@pytest.mark.capability("example.sum")
def test_the_firmware_adds(board, board_id):
    reply = board.send_cmd_awaiting("sum", lambda e: e["evt"] == "sum", "a sum", timeout=5, a=20, b=22)
    assert reply["value"] == 42, f"{board_id} says {reply}"
