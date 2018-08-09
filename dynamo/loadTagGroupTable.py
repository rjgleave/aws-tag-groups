from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('tagGroup')

with open("sample-data.json") as json_file:
    rows = json.load(json_file, parse_float = decimal.Decimal)
    for r in rows:
        # NOTE: enforce strings - in case user loaded numbers into their CSV and JSON converter 
        groupKey = str(r['GroupKey']) if r['GroupKey'] else "none"
        groupValue = str(r['GroupValue']) if r['GroupValue'] else "none"
        tagKey = str(r['TagKey']) if r['TagKey'] else "none"
        tagValue = str(r['TagValue']) if r['TagValue'] else "none"
        # create a range key composed of the other table elements.  This will provide a unique range key
        # for dynamo and also provide a natural sort to the table.  Useful as well for grouping.
        sort_list = []
        sort_list.append(groupKey)
        sort_list.append(str(groupValue))
        sort_list.append(tagKey)
        sort_list.append(str(tagValue))
        sortKey = os.path.join(*sort_list)
        #sortKey = r['SortKey'] if r['SortKey'] else "none"

        print("Adding record:", sortKey)

        table.put_item(
        Item={
            'groupKey': groupKey,
            'sortKey': sortKey,
            'groupValue': groupValue,
            'tagKey': tagKey,
            'tagValue': tagValue
            }
        )
