
from boto3 import resource
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone

dynamodb = resource("dynamodb", region_name="us-east-2")
events_table = dynamodb.Table("dynamo_calendar_events_2")


def create_event(calendar_id, event_id, name, date,
                 description="", difficulty=1):
    item = {
        "calendar_id": str(calendar_id),
        "event_id": str(event_id),
        "name": name,
        "description": description,
        "due_date": date,
        "difficulty": difficulty,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    events_table.put_item(Item=item)
    return item


def get_event(calendar_id, event_id):
    response = events_table.get_item(
        Key={
            "calendar_id": str(calendar_id)
        }
    )
    return response.get("Item")


def get_events_for_calendar(calendar_id):
    """Retrieve all events in one calendar"""
    response = events_table.query(
        KeyConditionExpression=Key("calendar_id").eq(str(calendar_id))
    )
    return response.get("Items", [])
