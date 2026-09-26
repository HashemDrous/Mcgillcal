"""
ics_writer.py
Writes events into a .ics file.

A .ics file is just plain text in a standard format (called iCalendar)
that Apple Calendar, Google Calendar and Outlook can all import.
A tiny example looks like this:

    BEGIN:VCALENDAR
    VERSION:2.0
    BEGIN:VEVENT
    SUMMARY:COMP 202
    DTSTART;TZID=America/Toronto:20260902T103500
    ...
    END:VEVENT
    END:VCALENDAR
"""

import datetime

# Montreal uses the same time zone as Toronto.
TIMEZONE = "America/Toronto"


def format_time(moment):
    """datetime(2026, 9, 2, 10, 35) -> '20260902T103500'"""
    return moment.strftime("%Y%m%dT%H%M%S")


def event_to_lines(event, number):
    """Turn one event dictionary into the list of text lines for it."""
    # Every event needs a unique ID so calendar apps don't mix them up.
    uid = "mcgill-cal-" + str(number) + "-" + format_time(event["start"])
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    return [
        "BEGIN:VEVENT",
        "UID:" + uid,
        "DTSTAMP:" + now,
        "SUMMARY:" + event["title"],
        "LOCATION:" + event["location"],
        "DTSTART;TZID=" + TIMEZONE + ":" + format_time(event["start"]),
        "DTEND;TZID=" + TIMEZONE + ":" + format_time(event["end"]),
        "RRULE:" + event["rule"],
        "END:VEVENT",
    ]


def build_calendar_text(events):
    """Build the full text of the .ics file."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//mcgill-cal//EN",
        "CALSCALE:GREGORIAN",
    ]

    number = 1
    for event in events:
        lines = lines + event_to_lines(event, number)
        number = number + 1

    lines.append("END:VCALENDAR")

    # The iCalendar standard wants lines to end with \r\n
    return "\r\n".join(lines) + "\r\n"


def write_ics(events, filename):
    """Save the calendar text into a file."""
    file = open(filename, "w", newline="")
    file.write(build_calendar_text(events))
    file.close()
