from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime


calendar_table = resource('dynamodb', region_name='us-east-2').Table('dynamodb-calendar-events')

def insert():
    response = calendar_table.put_item(
        Item={
            'user_id': 'cus-02', # partition key
            'order_id' : 'ord-3', # sort key
            'status': 'pending',
            'created_date' : datetime.now().isoformat()
        }
    )
    print(f'Insert responses: {response}')

insert()


def get_existing_item():
    response = calendar_table.get_item(
        Key={
            'user_id': 'cus-02',
            'order_id': 'ord-3'
        }
    )

    item = response.get('Item')

    if item:
        print("Found item:")
        print(item)
    else:
        print("Item not found.")

get_existing_item()
