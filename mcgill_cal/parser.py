"""
parser.py
Reads the schedule CSV file and turns each row into a dictionary.

Example row in the CSV:
    COMP 202,MWF,10:35,11:25,Leacock 132

Becomes this dictionary:
    {
        "course": "COMP 202",
        "days": ["M", "W", "F"],
        "start": "10:35",
        "end": "11:25",
        "room": "Leacock 132",
    }
"""

# McGill writes Thursday as "R" so it doesn't clash with Tuesday "T".
VALID_DAYS = "MTWRF"


def check_time(text):
    """Make sure a time looks like HH:MM (24-hour). Returns it cleaned up."""
    text = text.strip()
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("Time must look like HH:MM, got: " + text)

    hour = int(parts[0])
    minute = int(parts[1])
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("Time is out of range: " + text)

    # Always give back two digits each, e.g. "9:05" -> "09:05"
    return str(hour).zfill(2) + ":" + str(minute).zfill(2)


def parse_days(text):
    """Turn a string like 'MWF' into a list like ['M', 'W', 'F']."""
    days = []
    for letter in text.strip().upper():
        if letter not in VALID_DAYS:
            raise ValueError("Unknown day letter '" + letter + "'. Use M T W R F.")
        if letter not in days:  # skip duplicates like "MM"
            days.append(letter)
    return days


def parse_line(line):
    """Turn one line of the CSV into a course dictionary."""
    pieces = line.strip().split(",")
    if len(pieces) != 5:
        raise ValueError("Each row needs 5 columns: " + line)

    course = {
        "course": pieces[0].strip(),
        "days": parse_days(pieces[1]),
        "start": check_time(pieces[2]),
        "end": check_time(pieces[3]),
        "room": pieces[4].strip(),
    }

    # "09:00" < "10:00" works because both strings have the same format.
    if course["start"] >= course["end"]:
        raise ValueError(course["course"] + ": start time must be before end time")

    return course


def read_schedule(filename):
    """Read the whole CSV file and return a list of course dictionaries."""
    courses = []
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    # lines[0] is the header (course,days,start,end,room), so we skip it.
    for line in lines[1:]:
        if line.strip() == "":  # skip empty lines
            continue
        courses.append(parse_line(line))

    return courses
