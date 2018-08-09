from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

table = dynamodb.Table('tagGroup')

with open("sample-data.json") as json_file:
    rows = json.load(json_file, parse_float = decimal.Decimal)
    for r in rows:
        tagGroup = r['TagGroup'] if r['TagGroup'] else "none"
        sortKey = r['SortKey'] if r['SortKey'] else "none"
        groupKey = r['GroupKey'] if r['GroupKey'] else "none"
        groupValue = r['GroupValue'] if r['GroupValue'] else "none"
        tagKey = r['TagKey'] if r['TagKey'] else "none"
        tagValue = r['TagValue'] if r['TagValue'] else "none"

        print("Adding record:", sortKey)

        table.put_item(
        Item={
            'tagGroup': tagGroup,
            'sortKey': sortKey,
            'groupKey': groupKey,
            'groupValue': groupValue,
            'tagKey': tagKey,
            'tagValue': tagValue
            }
        )
