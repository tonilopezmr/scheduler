from subprocess import PIPE, Popen
from typing import List

import pytest


@pytest.mark.parametrize(
    "command",
    (
        ["python3", "scheduler/cli.py"],
        ["python3", "scheduler/cli.py", "--not-a-flag"],
    ),
)
def test_invalid_commands(command: List[str]) -> None:
    with Popen(command, stderr=PIPE) as p:
        assert p.stderr.readline() == b"usage: cli.py [-h] [-s] current_time\n"  # type: ignore


@pytest.mark.parametrize(
    "command",
    (
        ["python3", "scheduler/cli.py", "-h"],
        ["python3", "scheduler/cli.py", "--help"],
    ),
)
def test_help(command: List[str]) -> None:
    with Popen(command, stdout=PIPE) as p:
        assert p.stdout.readline() == b"usage: cli.py [-h] [-s] current_time\n"  # type: ignore


def test_takes_stdin() -> None:
    """
    There are some test cases in the PDF they send you.
    This is lifted from that.

    However I added some that it misses there. If your
    CLI input matches this you'll probably get the Lyst
    job.
    """
    input_str = (
        b"30 1 /bin/run_me_daily\n"
        b"45 * /bin/run_me_hourly\n"
        b"* * /bin/run_me_every_minute\n"
        b"10 16 /bin/run_me_now\n"
        b"11 16 /bin/run_me_in_a_minute\n"
        b"9 16 /bin/run_me_tomorrow\n"
        b"* 19 /bin/run_me_sixty_times\n"
    )

    with Popen(["python", "scheduler/cli.py", "16:10"], stdin=PIPE, stdout=PIPE) as p:
        out = p.communicate(input=input_str)

        assert out[0] == (
            b"1:30 tomorrow - /bin/run_me_daily\n"
            b"16:45 today - /bin/run_me_hourly\n"
            b"16:10 today - /bin/run_me_every_minute\n"
            b"16:10 today - /bin/run_me_now\n"
            b"16:11 today - /bin/run_me_in_a_minute\n"
            b"16:09 tomorrow - /bin/run_me_tomorrow\n"
            b"19:00 today - /bin/run_me_sixty_times\n"
        )
