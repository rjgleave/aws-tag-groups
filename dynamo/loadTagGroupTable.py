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
        tagKey1 = str(r['TagKey1']) if r['TagKey1'] else "none"
        tagValue1 = str(r['TagValue1']) if r['TagValue1'] else "none"
        tagKey2 = str(r['TagKey2']) if r['TagKey2'] else "none"
        tagValue2 = str(r['TagValue2']) if r['TagValue2'] else "none"
        tagKey3 = str(r['TagKey3']) if r['TagKey3'] else "none"
        tagValue3 = str(r['TagValue3']) if r['TagValue3'] else "none"
        tagKey4 = str(r['TagKey4']) if r['TagKey4'] else "none"
        tagValue4 = str(r['TagValue4']) if r['TagValue4'] else "none"
        tagKey5 = str(r['TagKey5']) if r['TagKey5'] else "none"
        tagValue5 = str(r['TagValue5']) if r['TagValue5'] else "none"
        # create a range key composed of the other table elements.  This will provide a unique range key
        # for dynamo and also provide a natural sort to the table.  Useful as well for grouping.
        sort_list = []
        sort_list.append(groupKey)
        sort_list.append(str(groupValue))
        sort_list.append(tagKey1)
        sort_list.append(str(tagValue1))
        sort_list.append(tagKey2)
        sort_list.append(str(tagValue2))
        sort_list.append(tagKey3)
        sort_list.append(str(tagValue3))
        sort_list.append(tagKey4)
        sort_list.append(str(tagValue4))
        sort_list.append(tagKey5)
        sort_list.append(str(tagValue5))
        sortKey = os.path.join(*sort_list)
        #sortKey = r['SortKey'] if r['SortKey'] else "none"

        print("Adding record:", sortKey)

        table.put_item(
        Item={
            'groupKey': groupKey,
            'sortKey': sortKey,
            'groupValue': groupValue,
            'tagKey1': tagKey1,
            'tagValue1': tagValue1,
            'tagKey2': tagKey2,
            'tagValue2': tagValue2,
            'tagKey3': tagKey3,
            'tagValue3': tagValue3,
            'tagKey4': tagKey4,
            'tagValue4': tagValue4,
            'tagKey5': tagKey5,
            'tagValue5': tagValue5,   
            }
        )
