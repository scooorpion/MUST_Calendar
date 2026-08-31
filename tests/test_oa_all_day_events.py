from datetime import date, datetime, timezone
from unittest import TestCase

from calendar_exporter import UnifiedCalendarExporter
from sources import MACAU_TIMEZONE, OAScheduleSource


class OAScheduleAllDayEventTests(TestCase):
    def setUp(self) -> None:
        self.source = OAScheduleSource("session-cookie")

    def test_single_day_leave_event_ignores_incorrect_api_flag(self) -> None:
        event = self.source._normalise_event(
            {
                "id": 1,
                "title": "澳門特別行政區成立紀念日",
                "eventType": "LEAVE_CALENDER",
                "isAllDay": False,
                "tempStartTime": "2026-12-20T00:00:00+0800",
                "tempEndTime": "2026-12-20T00:00:00+0800",
            }
        )

        self.assertIsNotNone(event)
        self.assertTrue(event.is_all_day)
        self.assertEqual(event.start, date(2026, 12, 20))
        self.assertEqual(event.end, date(2026, 12, 21))

    def test_multi_day_leave_event_uses_exclusive_ical_end_date(self) -> None:
        event = self.source._normalise_event(
            {
                "id": 2,
                "title": "聖誕節假期",
                "eventType": "LEAVE_CALENDER",
                "isAllDay": False,
                "tempStartTime": "2026-12-24T00:00:00+0800",
                "tempEndTime": "2026-12-25T00:00:00+0800",
            }
        )

        self.assertIsNotNone(event)
        self.assertTrue(event.is_all_day)
        self.assertEqual(event.start, date(2026, 12, 24))
        self.assertEqual(event.end, date(2026, 12, 26))

        calendar = UnifiedCalendarExporter("student").build(
            [event],
            generated_at=datetime(2026, 8, 31, tzinfo=timezone.utc),
        )
        ical = calendar.to_ical()
        self.assertIn(b"DTSTART;VALUE=DATE:20261224", ical)
        self.assertIn(b"DTEND;VALUE=DATE:20261226", ical)
        self.assertNotIn(b"BEGIN:VALARM", ical)

    def test_regular_midnight_event_remains_timed(self) -> None:
        event = self.source._normalise_event(
            {
                "id": 3,
                "title": "午夜日程",
                "eventType": "PERSONAL",
                "isAllDay": False,
                "tempStartTime": "2026-12-24T00:00:00+0800",
                "tempEndTime": "2026-12-25T00:00:00+0800",
            }
        )

        self.assertIsNotNone(event)
        self.assertFalse(event.is_all_day)
        self.assertEqual(
            event.start,
            datetime(2026, 12, 24, tzinfo=MACAU_TIMEZONE),
        )
        self.assertEqual(
            event.end,
            datetime(2026, 12, 25, tzinfo=MACAU_TIMEZONE),
        )

        calendar = UnifiedCalendarExporter("student").build(
            [event],
            generated_at=datetime(2026, 8, 31, tzinfo=timezone.utc),
        )
        ical = calendar.to_ical()
        self.assertIn(b"DTSTART:20261223T160000Z", ical)
        self.assertIn(b"DTEND:20261224T160000Z", ical)
        self.assertIn(b"BEGIN:VALARM", ical)
