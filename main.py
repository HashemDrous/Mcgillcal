"""
main.py
Entry point. Run it like this:

    python main.py schedule.csv

Optional: choose your own semester dates and output file name:

    python main.py schedule.csv 2026-09-01 2026-12-03 my_classes.ics
"""

import datetime
import sys

from mcgill_cal.parser import read_schedule
from mcgill_cal.events import make_all_events
from mcgill_cal.ics_writer import write_ics

# Default dates: first and last day of Fall 2026 classes.
# Double-check these against McGill's official key dates page!
DEFAULT_START = "2026-09-01"
DEFAULT_END = "2026-12-03"
DEFAULT_OUTPUT = "schedule.ics"


def to_date(text):
    """'2026-09-01' -> datetime.date(2026, 9, 1)"""
    year, month, day = text.split("-")
    return datetime.date(int(year), int(month), int(day))


def main():
    # sys.argv is the list of words typed after "python".
    # sys.argv[0] is "main.py", sys.argv[1] is the CSV file, and so on.
    if len(sys.argv) < 2:
        print("Usage: python main.py schedule.csv [start] [end] [output.ics]")
        return

    csv_file = sys.argv[1]
    start_text = DEFAULT_START
    end_text = DEFAULT_END
    output_file = DEFAULT_OUTPUT

    if len(sys.argv) >= 4:
        start_text = sys.argv[2]
        end_text = sys.argv[3]
    if len(sys.argv) >= 5:
        output_file = sys.argv[4]

    courses = read_schedule(csv_file)
    events = make_all_events(courses, to_date(start_text), to_date(end_text))
    write_ics(events, output_file)

    print("Created " + output_file + " with " + str(len(events)) + " courses:")
    for event in events:
        print("  " + event["title"] + "  first class: "
              + event["start"].strftime("%a %b %d at %H:%M"))
    print("Import it into Apple Calendar, Google Calendar or Outlook.")


if __name__ == "__main__":
    main()
