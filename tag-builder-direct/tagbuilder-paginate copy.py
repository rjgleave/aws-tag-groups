import boto3
import sys
import argparse

# set up dynamoDB table 
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('tagGroup')
# load tagging API
client = boto3.client('resourcegroupstaggingapi')

# find the list of resources which have the group tag
def lookup(key, value):


    def lookup_for_tags(token):
        response = client.get_resources(
            PaginationToken=token,
            TagFilters=[
                {
                    'Key': key,
                    'Values': [value]
                }
            ],
            ResourcesPerPage=50
        )
        return response

    def update_tags(a_list):
        #print "alist is:", a_list
        print "Tagging resources..."
        response = client.tag_resources(
            ResourceARNList=a_list,
            Tags={
                'BudgetCode': 'PROJECT-12345',
                'EBSCostCenter': '4000003',
                'LOB': 'Fund'
            }
        )
        print "Done!"
        return response


    total_results = []
    response = lookup_for_tags("")
    #print response
    page_token = ""
    
    while True:
        total_results += response["ResourceTagMappingList"]
        page_token = response["PaginationToken"]
        if page_token == "":
            break
        response = lookup_for_tags(page_token)
       
    arn_list=[]
    for r in total_results:
        print "Reading resource: ",r["ResourceARN"]
        arn_list.append(r["ResourceARN"])

    # Update the Tags Based for the list of resources
    resp = update_tags(arn_list)



# determine the list of tags to read
def read_table(tag_group_name, tag_list):

    ddb_response = table.query(
        KeyConditionExpression=Key('GroupName').eq(tag_group_name) 
    )
    # get the unique group keys
    for r in ddb_response:

    return ddb_response, tag_list


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="ec2_lookup",
        description="Search for EC2 instances based on tags.",
    )
    parser.add_argument('--tag_name', default="AppName", help="The name of the tag to filter on")
    parser.add_argument('tag_value', help="The value of the tag to filter on")

    return parser.parse_args(args)


def main():
    # get command line parameters
    cli_args = sys.argv[1:]
    args = parse_args(cli_args)

    # set global variables
    tag_group_name = 'Finance'

    # read tagGroup table 
    ddb_response = table.query(
        KeyConditionExpression=Key('tagGroup').eq(tag_group_name) 
    )
    #tag_list = read_table(tag_list)
    #print("Tag group list: " + tag_list)
    print ddb_response

    # create a dictionary for the job array
    jobArray = {}

    # read all job steps for the schedule
    for i in ddb_response['Items']:
        # create class objects
        if i['RecordType'] == 'HEADER':
            jsch = JsSchedule(i['ScheduleName'],i['Description'], "running", {})
            continue   
        elif i['RecordType'] == 'JOB':
            jjob = JsJob(i['JobName'],i['Command'],i['JobDependencies'])         
        else:
            print "Invalid RecordType in Schedule table >>: ", i['RecordType']
            continue
        JobName = i['JobName']

        # find resources with the groupKey
        lookup(args.tag_name, args.tag_value)

        # add the current job/JobID key/value pairs to the list of submitted jobs
        jsch.JobArray[jjob.JobName] = s_resp['jobId']

        print("Submitted Job: {}, JobId: {}, Runs After: {}".format(jjob.JobName,s_resp['jobId'],str(jjob.JobDependencies)))    



if __name__ == '__main__':
    main()