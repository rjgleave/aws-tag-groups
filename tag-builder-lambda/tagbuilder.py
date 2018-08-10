import boto3
import sys
import argparse
import os

# set up dynamoDB table 
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('tagGroup')
# load tagging API
client = boto3.client('resourcegroupstaggingapi')

# NOTE: YOU MUST SET UP THE TAG GROUP_KEY ENVIRONMENT VARIABLE IN THE LAMBDA!
# example:   GROUP_KEY = 'TagGroup' (no quotes needed in Lambda console)
# import Environment Variables for Lambda configuration
group_key = os.environ['GROUP_KEY']

# read all the records in the tagGroup table
def read_table(tag_group_key):
    # read tagGroup table 
    response = table.query(
        KeyConditionExpression=Key('groupKey').eq(tag_group_key) 
    )
    return response

# find and tag resources
def mass_update(group_key, group_value, tag_list):

    # find the resources with the tag key/value combination 
    def find_resources(token):
        page_size = 50
        # search using the API
        response = client.get_resources(
            PaginationToken=token,
            TagFilters=[
                {
                    'Key': group_key,
                    'Values': [group_value]
                }
            ],
            ResourcesPerPage=page_size
        )

        # PAGINATION: this is important as the number of resources grows
        # save the page token (if there is more to read)
        page_token = response["PaginationToken"]

        ## create a list of ARNs
        # first: get just the resources from the response
        rlist = response['ResourceTagMappingList']
        # second: pull out just the ARNs
        arn_list=[]      
        for r in rlist:
            #print "Reading resource: ",r["ResourceARN"]
            arn_list.append(r["ResourceARN"])

        return arn_list, page_token

    # add the list of tags to all resources
    def update_resources(arn_list, tag_list):
        print "Tagging resources..."
        try:
            response = client.tag_resources(
                ResourceARNList = arn_list,
                Tags = tag_list
            )
        print('Tagging resources {} with tags {}'.format(arn_list, tag_list))
        except Exception as e:
            print(e)
            print('Error tagging resources {} with tags {}'.format(arn_list, tag_list))
        #raise e
        #print 'Tag Response >>>>', response

        return response

    # search for resources needing tags
    arn_list, page_token = find_resources("")
    
    while True:
        if arn_list:
            # update the resources with the list of required tags
            u_response = update_resources(arn_list, tag_list)

            # check to see there are more pages 
            if page_token == "":
                break
            # search for more resources
            arn_list, page_token = find_resources(page_token)
        else:
           break


def lambda_handler(event, context):

    # read the tagGroup table
    ddb_response = read_table(group_key)
 
    # read all job steps for the schedule.  To minimize API calls, collect all tags 
    # which need to be applied before calling the API 
    last_gv = ""
    last_list={}
    print "Reading Table..." 
    for i in ddb_response['Items']:
        print i['groupKey'], i['groupValue'], i['tagKey'], i['tagValue']
        # create class objects
        if i['groupValue'] != last_gv:
            # run mass update 
            if last_gv > 0 and len(last_list) > 0:
                mass_update(group_key, last_gv, last_list)
            # reset last values
            last_gv = i['groupValue'] 
            last_list = {}      

        # add the tag to the list
        tdict={}
        tdict[i['tagKey']]=i['tagValue']
        last_list.update(tdict)

    # run final mass update 
    if last_gv > 0 and len(last_list) > 0:
        mass_update(group_key, last_gv, last_list) 


    return "Tag update complete"