from datetime import datetime

import pytest

from scheduler.parser import CronDefinition, ParserException, parse_line


class TestAbsoluteTimes:
    def test_before_time(self) -> None:
        current_time = datetime(year=1900, month=1, day=1)
        definition = CronDefinition(hour=1, minute=30, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 1, 30)

    def test_exact_time(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=1, minute=30)
        definition = CronDefinition(hour=1, minute=30, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 1, 30)

    def test_after_time(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=3)
        definition = CronDefinition(hour=1, minute=30, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 2, 1, 30)


class TestHourlyTimes:
    def test_before_minute(self) -> None:
        current_time = datetime(year=1900, month=1, day=1)
        definition = CronDefinition(hour=None, minute=30, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 0, 30)

    def test_exact_minute(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=23, minute=30)
        definition = CronDefinition(hour=None, minute=30, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 23, 30)

    def test_after_minute(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=0, minute=31)
        definition = CronDefinition(hour=None, minute=30, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 1, 30)


class TestMinuteTimes:
    def test_before_hour(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=0)
        definition = CronDefinition(hour=1, minute=None, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 1, 0)

    def test_at_start_of_hour(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=1)
        definition = CronDefinition(hour=1, minute=None, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 1, 0)

    def test_during_hour(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=1, minute=5)
        definition = CronDefinition(hour=1, minute=None, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 1, 1, 5)

    def test_after_hour(self) -> None:
        current_time = datetime(year=1900, month=1, day=1, hour=2, minute=5)
        definition = CronDefinition(hour=1, minute=None, command="")
        time = definition.get_next_time(current_time)
        assert time == datetime(1900, 1, 2, 1, 0)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("1 2 abc", CronDefinition(2, 1, "abc")),
        ("* 2 abc", CronDefinition(2, None, "abc")),
        ("2 * abc", CronDefinition(None, 2, "abc")),
        ("0 * abc", CronDefinition(None, 0, "abc")),
        ("* * abc", CronDefinition(None, None, "abc")),
    ],
)
def test_valid_inputs(input_str: str, expected: CronDefinition) -> None:
    assert parse_line(input_str) == expected


@pytest.mark.parametrize("input_str", ["1", "1 *", "\n", "", "70 2 abc"])
def test_invalid_inputs(input_str: str) -> None:
    with pytest.raises(ParserException):
        parse_line(input_str)
