
from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')


table = dynamodb.create_table(
    TableName='tagGroup',
    KeySchema=[
        {
            'AttributeName': 'tagGroup',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'sortKey',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'tagGroup',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'sortKey',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
