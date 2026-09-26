# mcgill-cal 📅

Turn your McGill class schedule into a calendar file you can import into
**Apple Calendar, Google Calendar or Outlook** — every lecture repeats
weekly until the end of the semester, with the room as the location.

Pure Python. No libraries to install.

![screenshot](screenshot.png)

## How it works

```
schedule.csv  →  parser.py  →  events.py  →  ics_writer.py  →  schedule.ics
 (your classes)   (reads CSV)   (weekly repeats)  (writes file)   (import this)
```

| File | Job |
|------|-----|
| `mcgill_cal/parser.py` | Reads each CSV row into a dictionary and checks it (valid days, times, start before end). |
| `mcgill_cal/events.py` | Finds each course's first class date and builds a weekly repeat rule. |
| `mcgill_cal/ics_writer.py` | Writes the events in the iCalendar (`.ics`) format calendar apps understand. |
| `main.py` | Runs everything from the command line. |
| `tests/test_events.py` | Unit tests for the logic. |

## Input format

Edit `schedule.csv`. Days use McGill's letters: **M T W R F** (R = Thursday).

```
course,days,start,end,room
COMP 202,MWF,10:35,11:25,Leacock 132
MATH 133,TR,11:35,12:55,Burnside 1B45
```

## How to run

```bash
python main.py schedule.csv
```

Output:

```
Created schedule.ics with 4 courses:
  COMP 202  first class: Wed Sep 02 at 10:35
  MATH 133  first class: Tue Sep 01 at 11:35
  ...
```

Custom semester dates and output name:

```bash
python main.py schedule.csv 2026-09-01 2026-12-03 fall2026.ics
```

Then double-click `schedule.ics` (Apple Calendar) or use *Import* in Google Calendar.

> Default dates are Fall 2026 (Sep 1 – Dec 3). Check them against McGill's official key dates.

## Run the tests

```bash
python -m unittest discover tests
```

## Ideas for next versions

- Skip holidays and reading week (`EXDATE` lines)
- Read the schedule straight from a Minerva export
- Add tutorials and labs with a `type` column
