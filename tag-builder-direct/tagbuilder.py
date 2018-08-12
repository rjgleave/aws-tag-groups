import boto3
import sys
import argparse

# set up dynamoDB table 
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('tagGroup')
# load tagging API
client = boto3.client('resourcegroupstaggingapi')

# read all the records in the tagGroup table
def read_table(tag_group_key):
    # read tagGroup table 
    response = table.query(
        KeyConditionExpression=Key('groupKey').eq(tag_group_key) 
    )
    return response

# create a dictionary to hold the tag list for filtering 
def create_filter_list(row):
    f_tag_dict = {}
    for x in range(len(row)):
        key_column_name = "tagKey" + str(x)
        value_column_name = "tagValue" + str(x)   
        k = row.get(key_column_name, 'not found')
        v = row.get(value_column_name, 'not found')   
        #print  key_column_name, value_column_name, k, v
        if k != 'none' and k != 'not found':
            f_tag_dict[k]=v

    return f_tag_dict

# find the resources with the tag key/value combination 
def find_resources(group_key, group_value, filter_list, filter_on):
    # search using the API
    response = client.get_resources(
        TagFilters=[
            {
                'Key': group_key,
                'Values': [group_value]
            }
        ]
    )
    # get just the resources from the response
    rlist = response['ResourceTagMappingList']
    
    # build lists of ARNs and Tags
    r_arn_list=[]     
    r_tag_list={}
    for r in rlist:
        #print "Reading resource: ",r["ResourceARN"], r["Tags"]
        # reformat tags into key/value dictionary
        rtags = r["Tags"]
        temp_dict = {}
        for i in rtags:
            temp_dict[i['Key']]=i['Value']

        # filter logic - if ON, then check for tag compliance.  If OFF, then all are non-compliant
        if filter_on:
            tags_compliant = all(item in temp_dict.items() for item in filter_list.items())
        else:
            tags_compliant = False
            
        #print "Tags compliant? ", tags_compliant
        if not tags_compliant:
                #r_tag_list.update(r_tag_list)
                r_arn_list.append(r["ResourceARN"])

    return r_arn_list


# find and tag resources
def tag_update(resource_arn_list, tag_list):

    # update the tags on the non-compliant resources
    def update_resources(arn_list, tag_list):
        print 'updating: ', arn_list
        response = client.tag_resources(
            ResourceARNList = arn_list,
            Tags = tag_list
        )
        return response
    
    # apply tags to all resources in the list
    for r in resource_arn_list:
        # you can only update 20 resources at a time
        for x in range(0,len(resource_arn_list), 20):
            sub_list = resource_arn_list[x: x+20]
            # update the resources with the list of required tags
            u_response = update_resources(sub_list, tag_list)


def main():

    # set global variables
    group_key = 'TagGroup'
    filter_on = True

    print "Tag Filter ON?: ", filter_on
    
    # read the tagGroup table
    ddb_response = read_table(group_key)
 
    # read all control records for the tag group
    f_tag_dict={}
    for i in ddb_response['Items']:
        print "Processing.. {}/{}".format(i['groupKey'],i['groupValue'])

        # create a tag list from the dynamo record
        f_tag_dict = create_filter_list(i)

        print "Filter list", f_tag_dict

        # find all resources with the group key and value
        resource_arn_list = find_resources(i['groupKey'],i['groupValue'], f_tag_dict, filter_on)

        # run mass update 
        if resource_arn_list:
            #print "ARN list", resource_arn_list
            #print "Tag list", resource_tag_list[0]
            tag_update(resource_arn_list, f_tag_dict)     

if __name__ == '__main__':
    main()