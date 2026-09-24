"""The suite's fixtures. The rig's pytest plugin (installed with
`alteriom-hil`) provides `bank`: one board client per board the run was
given, each already checked responsive. Two things are added here.

`board` turns the bank into one test row per board, so a report says which
board failed rather than that something did -- the pattern the rig's own
health check uses.

`sim_firmware` teaches the rig's simulator this firmware's own command, so
the suite runs in this repository's CI with no board attached
(ALTERIOM_HIL_MODE=sim). A simulated pass is evidence about the suite, never
about an ESP; the tests say so with `hil_only`."""

from __future__ import annotations

import os

import pytest
from alteriom_hil.sim import SimFirmware


class ExampleFirmware(SimFirmware):
    """What the simulated board answers beyond `info`, `echo` and `reset`:
    the same `sum` the real firmware answers."""

    def handle(self, board, name: str, cmd: dict) -> bool:
        if name == "sum":
            a, b = int(cmd.get("a", 0)), int(cmd.get("b", 0))
            board.emit({"evt": "sum", "a": a, "b": b, "value": a + b})
            return True
        return False


@pytest.fixture(scope="session")
def sim_firmware():
    return ExampleFirmware


def pytest_generate_tests(metafunc):
    """One row per board. Collection happens before any fixture runs, so the
    board ids come from the board map the rig hands the run (hardware) or
    from the simulator's count (sim)."""
    if "board_id" not in metafunc.fixturenames:
        return
    if os.environ.get("ALTERIOM_HIL_MODE") != "hardware":
        count = int(os.environ.get("ALTERIOM_HIL_SIM_BOARDS", "3"))
        ids = [f"sim-{1000 + index}" for index in range(count)]
    else:
        from alteriom_hil.board import BoardMap

        path = os.environ.get("ALTERIOM_HIL_BOARD_MAP")
        ids = [board.id for board in BoardMap.load(path)] if path else []
    metafunc.parametrize("board_id", ids)


@pytest.fixture()
def board(board_id, bank):
    """The client for the board this row is about."""
    client = bank.get(board_id)
    if client is None:
        pytest.fail(f"board {board_id} was collected but the bank has no client for it")
    client.clear_pending()
    return client
