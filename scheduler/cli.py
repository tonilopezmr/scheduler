import argparse
from datetime import datetime
import logging
import sys

from scheduler.parser import CronDefinition, ParserException, parse_line

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Scheduler file tester")

parser.add_argument("current_time", action="store", type=str)
parser.add_argument(
    "-s", "--strict", action="store_true", default=False, help="Terminate if error found"
)


def format_next_time(
    next_time: datetime, current_time: datetime, definition: CronDefinition
) -> str:
    day = "today"

    if next_time.day > current_time.day:
        day = "tomorrow"

    return "{time} {day} - {command}".format(
        time=next_time.strftime("%-H:%M"), day=day, command=definition.command
    )


def main() -> None:
    parser_args = parser.parse_args()
    current_time = parser_args.current_time
    current_time = datetime.strptime(current_time, "%H:%M")

    for idx, line in enumerate(sys.stdin):

        try:
            definition = parse_line(line)
            next_time = definition.get_next_time(current_time)
            print(format_next_time(next_time, current_time, definition))
        except ParserException as e:
            if parser_args.strict:
                raise e
            else:
                logger.warning(f"Line {idx}: Parser Error:" + str(e))


if __name__ == "__main__":
    main()
