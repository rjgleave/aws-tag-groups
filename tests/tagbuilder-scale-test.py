import boto3
import sys
import argparse

# set up the SQS queue
import json
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='resourceAPIQueue')

# if this is True, then the tag updates will be queued to SQS
sqs_enabled = True


# option b: send a message via SQS to call the api at a throttled rate
def send_update_message(message_payload):
    #print "payload: ", json.dumps(message_payload)
    response = queue.send_message(
        MessageBody=json.dumps(message_payload)
    )
    return response     


def main():

    # sample batch of 20 resources to be updated
    payload = {"arn_list": ["arn:aws:ec2:us-east-2:786247309603:snapshot/snap-055f8cb589ba81feb", "arn:aws:ec2:us-east-2:786247309603:snapshot/snap-0da02d80d87a28187", "arn:aws:ec2:us-east-2:786247309603:volume/vol-05a0dba18a3b37ff2", "arn:aws:ec2:us-east-2:786247309603:snapshot/snap-025a8b70b3f0bc188", "arn:aws:ec2:us-east-2:786247309603:instance/i-042c953804da53443", "arn:aws:ec2:us-east-2:786247309603:instance/i-008209845c755399b", "arn:aws:ec2:us-east-2:786247309603:snapshot/snap-0ea7f2b8eeb4236ed", "arn:aws:s3:::migration-rjg-migrationstackbucket4blog", "arn:aws:ec2:us-east-2:786247309603:instance/i-07155d88aca5cc237", "arn:aws:dynamodb:us-east-2:786247309603:table/jobSchedule", "arn:aws:s3:::petminder-deployments-mobilehub-1107226580", "arn:aws:ec2:us-east-2:786247309603:instance/i-06e3e81d23c68dd80", "arn:aws:dynamodb:us-east-2:786247309603:table/tagGroup", "arn:aws:ec2:us-east-2:786247309603:volume/vol-064a1adc9fa8e7507", "arn:aws:ec2:us-east-2:786247309603:volume/vol-06b6517084128eae4", "arn:aws:ec2:us-east-2:786247309603:volume/vol-06c2722a9ff53ffbb", "arn:aws:ec2:us-east-2:786247309603:volume/vol-0a4195ba9557c8d4d", "arn:aws:s3:::cf-templates-8mxauch1fvup-us-east-2", "arn:aws:s3:::rjg-config-bucket", "arn:aws:s3:::rjg-created-with-cloudformation"], "tag_list": {"BudgetCode": "PROJECT-1212121", "EBSCostCenter": "4000009"}}
    # number of messages to test
    max_messages = 250

    print "SQS Enabled?: ", sqs_enabled

    for i in range(1,max_messages+1):
        print "Processing.. batch# {}".format(i)
        m_response = send_update_message(payload)    

if __name__ == '__main__':
    main()