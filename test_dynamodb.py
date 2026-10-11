
from dynamodb_events import (
    create_event,
    get_event,
    get_events_for_calendar
)

# test the calendar
calendar_id = "test-calendar-01"
event_id = "test-event-01"

# create an event
created = create_event(
    calendar_id=calendar_id,
    event_id=event_id,
    name="Finish homework",
    date="2026-10-12T14:00:00",
    description="Exercise 5",
    difficulty=5
)
print("Created:", created)

# find specific event
found = get_event(calendar_id, event_id)
print("Retrieved:", found)
assert found is not None
assert found["name"] == "Finish homework"

# retrieve the events from the calendar
events = get_events_for_calendar(calendar_id)
print("Events in calendar:", events)
assert any(event["event_id"] == event_id for event in events)

