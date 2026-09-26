"""
test_events.py
Small checks that the logic works. Run from the project folder with:

    python -m unittest discover tests
"""

import datetime
import unittest

from mcgill_cal.parser import parse_days, parse_line, check_time
from mcgill_cal.events import first_class_date, repeat_rule, make_event
from mcgill_cal.ics_writer import build_calendar_text


class TestParser(unittest.TestCase):

    def test_parse_days(self):
        self.assertEqual(parse_days("MWF"), ["M", "W", "F"])
        self.assertEqual(parse_days("tr"), ["T", "R"])  # lowercase is OK

    def test_bad_day_letter(self):
        with self.assertRaises(ValueError):
            parse_days("MX")

    def test_check_time_adds_zero(self):
        self.assertEqual(check_time("9:05"), "09:05")

    def test_start_after_end_is_error(self):
        with self.assertRaises(ValueError):
            parse_line("COMP 202,MWF,11:00,10:00,Leacock 132")


class TestEvents(unittest.TestCase):

    def test_first_class_same_day(self):
        # Sep 2 2026 is a Wednesday; a Wednesday class starts that day.
        start = datetime.date(2026, 9, 2)
        self.assertEqual(first_class_date(start, ["W"]), start)

    def test_first_class_later_in_week(self):
        # Sep 1 2026 is a Tuesday; a MWF class first meets Wed Sep 2.
        start = datetime.date(2026, 9, 1)
        self.assertEqual(first_class_date(start, ["M", "W", "F"]),
                         datetime.date(2026, 9, 2))

    def test_first_class_next_week(self):
        # Semester starts Friday Sep 4; a Monday-only class meets Sep 7.
        start = datetime.date(2026, 9, 4)
        self.assertEqual(first_class_date(start, ["M"]),
                         datetime.date(2026, 9, 7))

    def test_repeat_rule(self):
        rule = repeat_rule(["T", "R"], datetime.date(2026, 12, 3))
        self.assertEqual(rule, "FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20261203T235959")

    def test_make_event_times(self):
        course = parse_line("MATH 133,TR,11:35,12:55,Burnside 1B45")
        event = make_event(course, datetime.date(2026, 9, 1),
                           datetime.date(2026, 12, 3))
        self.assertEqual(event["start"], datetime.datetime(2026, 9, 1, 11, 35))
        self.assertEqual(event["end"], datetime.datetime(2026, 9, 1, 12, 55))


class TestIcsWriter(unittest.TestCase):

    def test_calendar_has_one_event_per_course(self):
        course = parse_line("COMP 202,MWF,10:35,11:25,Leacock 132")
        event = make_event(course, datetime.date(2026, 9, 1),
                           datetime.date(2026, 12, 3))
        text = build_calendar_text([event, event])

        self.assertTrue(text.startswith("BEGIN:VCALENDAR"))
        self.assertEqual(text.count("BEGIN:VEVENT"), 2)
        self.assertIn("SUMMARY:COMP 202", text)


if __name__ == "__main__":
    unittest.main()
