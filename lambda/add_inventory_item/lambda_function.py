import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import uuid

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
TABLE_NAME = 'Inventory'

def lambda_handler(event, context):

    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    table = dynamodb.Table(TABLE_NAME)

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    try:
        table.put_item(
            Item={
                'id': unique_id,
                'location_id': Decimal(data['location_id']),
                'name': data['name'],
                'description': data['description'],
                'price': Decimal(str(data['price'])),
                'qty': int(data['qty'])
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
