import boto3
import sys
import argparse

client = boto3.client('resourcegroupstaggingapi')

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
        print "alist is:", a_list
        response = client.tag_resources(
            ResourceARNList=a_list,
            Tags={
                'accounting-code': 'AA-12345',
                'cost-center': 'App-Dev'
            }
        )
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
        #print r["ResourceARN"]
        arn_list.append(r["ResourceARN"])

    #print arn_list
    resp = update_tags(arn_list)


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="ec2_lookup",
        description="Search for EC2 instances based on tags.",
    )
    parser.add_argument('--tag_name', default="Stage", help="The name of the tag to filter on")
    parser.add_argument('tag_value', help="The value of the tag to filter on")

    return parser.parse_args(args)


def main():
    cli_args = sys.argv[1:]
    args = parse_args(cli_args)
    lookup(args.tag_name, args.tag_value)


if __name__ == '__main__':
    main()