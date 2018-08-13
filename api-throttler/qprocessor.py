# qprocessor - this lambda is fired by a trigger from SQS.  It reads tag update messages from the queue 
# and uses the AWS ResourceGroupAPI to update tags on resources.

'''
Message Body - up to 20 resources in the arn_list
=========================================================================
{
    "arn_list": [
        "arn:aws:ec2:us-east-2:786247309603:instance/i-008209845c755399b"
    ],
    "tag_list": {
        "BudgetCode": "PROJECT-1212121",
        "EBSCostCenter": "4000009"
    }
}
=========================================================================
'''

import boto3
import sys
import os
import ast

# NOTE: YOU MUST SET UP THE ENVIRONMENT VARIABLES IN THE LAMBDA!
# example:   GROUP_KEY = 'TagGroup' (no quotes needed in Lambda console)
# import Environment Variables for Lambda configuration

# load tagging API
client = boto3.client('resourcegroupstaggingapi')

# update the tags on the non-compliant resources
def update_resources(arn_list, tag_list):
    print 'updating: ', arn_list, tag_list
    response = client.tag_resources(
        ResourceARNList = arn_list,
        Tags = tag_list
    )
    print response

    return response

### main lambda handler
def lambda_handler(event, context):
    for record in event['Records']:
        body = record['body']
        print(record['body'])

    b = {}
    b = ast.literal_eval(body)
    # parse body into components
    arn_list = b.get("arn_list", 'not found')
    tag_list = b.get("tag_list", 'not found')

    print "Processing.. arn-list: {} tag-list: {}".format(arn_list,tag_list)
    #print "arn_list", arn_list
    #print "tag_list", tag_list

    # run mass update 
    if arn_list and tag_list:
        # update the resources with the list of required tags
        u_response = update_resources(arn_list, tag_list)

    return "Tag update complete"
