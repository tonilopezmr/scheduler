from datetime import datetime, time, timedelta
import re
from typing import NamedTuple, Optional


class ParserException(Exception):
    pass


class InvalidLineFormat(ParserException):
    pass


class InvalidHour(ParserException):
    pass


class InvalidMinute(ParserException):
    pass


config_line_regex = re.compile(
    r"([ \t]+)?"  # optional - match all whitespace
    r"(?P<minute>[^\s]+)"  # match all up to next whitespace
    r"([ \t]+)"  # match all whitesapce
    r"(?P<hour>[^\s]+)"  # match all up to next whitespace
    r"([ \t]+)"  # match all up to next whitespace
    r"(?P<command>.*)"  # match all to end of input
)


class CronDefinition(NamedTuple):
    hour: Optional[int]
    minute: Optional[int]
    command: str

    def get_next_time(self, current_time: datetime) -> datetime:
        next_time = datetime.combine(current_time.date(), time(self.hour or 0, self.minute or 0))

        if self.hour and self.minute:
            if next_time < current_time:
                return next_time + timedelta(days=1)

        # if no hour, run on the current hour
        if not self.hour:
            next_time = next_time.replace(hour=current_time.hour)

        # else we have passed that hour and we go to the next day
        elif self.hour < current_time.hour:
            next_time = next_time + timedelta(days=1)

        # if no minute, run on the current minute
        if not self.minute:
            if current_time >= next_time:
                next_time = next_time.replace(minute=current_time.minute)
        # if current time is after the trigger run it the next hour
        elif self.minute < current_time.minute:
            next_time = next_time + timedelta(hours=1)

        return next_time


def _check_wildcard(num_value: str) -> Optional[str]:
    return None if num_value == "*" else num_value


def parse_line(line: str) -> CronDefinition:
    match = config_line_regex.match(line)
    if not match:
        raise InvalidLineFormat(
            "Line must follow the format: \n\n" "\t 0 0 command\n\n" "You have:\n\n" f"\t{line}"
        )

    lexed_input = match.groupdict()

    hour = _check_wildcard(lexed_input["hour"])
    minute = _check_wildcard(lexed_input["minute"])
    command = lexed_input["command"]

    # This is kind of crude because times have edge cases
    # that don't follow this validation scheme. However,
    # the python datetime module (as I checked) does not
    # account for things like leap seconds. So validating
    # time more comprehensively while using the datetime
    # module would be pointless.
    if hour:
        hour = int(hour)  # type: ignore
        if not 0 <= hour <= 23:  # type: ignore
            raise InvalidHour("Hour must be between 0 and 23")

    if minute:
        minute = int(minute)  # type: ignore
        if not 0 <= minute <= 59:  # type: ignore
            raise InvalidMinute("Minute must be between 0 and 59")

    return CronDefinition(hour, minute, command)  # type: ignore
