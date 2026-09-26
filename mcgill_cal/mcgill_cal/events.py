"""
events.py
Turns each course into a weekly repeating calendar event.

Idea: a course that meets "MWF" needs ONE event that repeats every
Monday, Wednesday and Friday until the end of the semester.

To do that we need:
  1. The FIRST date the class happens (on or after the semester start).
  2. A repeat rule that calendar apps understand, e.g.
     FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20261203T235959
"""

import datetime

# Our letters (M T W R F)  ->  Python's weekday numbers (Monday = 0)
DAY_NUMBER = {"M": 0, "T": 1, "W": 2, "R": 3, "F": 4}

# Our letters  ->  the 2-letter codes calendar files use
DAY_CODE = {"M": "MO", "T": "TU", "W": "WE", "R": "TH", "F": "FR"}


def first_class_date(semester_start, days):
    """
    Find the first date on or after semester_start that is one of `days`.

    Example: the semester starts on a Tuesday and the class is "MWF"
    -> the first class is Wednesday (the next day).
    """
    date = semester_start
    # At most 7 days until we hit a matching weekday.
    for i in range(7):
        for letter in days:
            if date.weekday() == DAY_NUMBER[letter]:
                return date
        date = date + datetime.timedelta(days=1)

    raise ValueError("No valid days given")


def repeat_rule(days, semester_end):
    """Build the weekly repeat rule text for a calendar file."""
    codes = []
    for letter in days:
        codes.append(DAY_CODE[letter])

    until = semester_end.strftime("%Y%m%d") + "T235959"
    return "FREQ=WEEKLY;BYDAY=" + ",".join(codes) + ";UNTIL=" + until


def make_event(course, semester_start, semester_end):
    """Turn one course dictionary into one event dictionary."""
    first_day = first_class_date(semester_start, course["days"])

    start_hour, start_minute = course["start"].split(":")
    end_hour, end_minute = course["end"].split(":")

    start = datetime.datetime(first_day.year, first_day.month, first_day.day,
                              int(start_hour), int(start_minute))
    end = datetime.datetime(first_day.year, first_day.month, first_day.day,
                            int(end_hour), int(end_minute))

    return {
        "title": course["course"],
        "location": course["room"],
        "start": start,
        "end": end,
        "rule": repeat_rule(course["days"], semester_end),
    }


def make_all_events(courses, semester_start, semester_end):
    """Turn a list of courses into a list of events."""
    if semester_start > semester_end:
        raise ValueError("Semester start must be before semester end")

    events = []
    for course in courses:
        events.append(make_event(course, semester_start, semester_end))
    return events
