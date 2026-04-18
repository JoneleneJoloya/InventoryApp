import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
TABLE_NAME = 'Inventory'
GSI_NAME = 'GSI_SK_PK'

# Function to convert Decimal to int/float
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):  
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    return obj

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    try:
        # use id instead of location_id to match with API Gateway resources
        user_input = event['pathParameters']['id']
        
        # Query to get all items with location_id(SK) using the GSI_SK_PK
        response = table.query(
            IndexName=GSI_NAME,
            KeyConditionExpression=Key('location_id').eq(int(user_input))
        )
        items = response.get('Items', [])

        # Convert Decimal values to JSON serializable types
        items = convert_decimals(items)

    except ClientError as e:
        print(f"Failed to query items: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to query items')
        }

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }