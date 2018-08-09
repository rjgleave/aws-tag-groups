Tag Group Application
==================================================

This solution will allow you to define tag groups, which can be used to automatically apply multiple tags to resources which are identified with a specific tag key.  The lambda uses the AWS Resource Group tagging API to efficiently search for resources and apply groups of tags to them.  This service provides powerful filtering capability and will automatically be updated by AWS as new services are added to the platform.   It also provides a powerful API for applying groups of tags to groups of resources with a single operation.

This design includes support for pagination, to support scaling to very large numbers of resources.  It will also make it relatively painless to decouple the updates using SQS, etc. if that is desired in the future.

What's Here
-----------

This repo includes:

* README.md - this file
* FOLDER: dynamo - this contains code to help build the tag group table in dynamoDB.  It includes:
 *   createTagGroupTable.py - a program to create the base dynamo table
 *   DataEntryTemplate.xlsx - an Excel template with sample data for the dynamo table
 *   sample-data.csv - a CSV extract of the excel file above
 *   sample-data.json - a JSON equivalent to the CSV file above
 *   loadTagGroupTable.py - a program to load the dynamodb table with sample data
* FOLDER: tag-builder-direct  - It includes:
 *   tagbuilder.py - the main lambda program to update resources with tags.  
* FOLDER: tag-builder-lambda - It includes:
 *   tagbuilder-paginate.py - same as lambda program above, except can be called from command line.

Step by Step Instructions
-------------------------

First, follow these steps to load the database:
1 - enter your sample data into the spreadsheet: DataEntryTemplate.xlsx
2 - export your data from the spreadsheet into a CSV file named: sample-data.csv
3 - convert the CSV file to JSON format.  The output file should be named: sample-data.json. You can do this with any online site such as:  http://www.convertcsv.com/csv-to-json.htm
4 - Run the program to create the dynamodb table: createTagGroupTable.py
5 - Run the program to load the data into the new table:  loadTagGroupTable.py
6 - Verify that the tagGroup table has been created in dynamoDB
7 - Create a service role for your lambda.   It should include at least the following policies:
 *   CloudwatchActionsEc2Access
 *   AWSResourceGroupsReadOnlyAccess
 *   AmazonDynamodbReadOnlyAccess
 *   AWSLambdaBasicExecutionRole
 *   ResourceGroupsandTagEditorFullAccess
6 - Install the lambda program in your chosen region. Configuration details below:
 *   Use the lambda role defined above
 *   create a trigger using Cloudwatch Events
 *   define the Cloudwatch Event with your lambda as a target.  The event should include a schedule of whatever frequency you prefer.
 *   create an Environment Variable with the Group key to filter resources.   The variable name must be GROUP_KEY.   The value can be whatever you like (see image below)


![Environment Variable](https://github.com/rjgleave/aws-tag-groups/blob/master/group-key-environment-variable.png)

__Additional Resources__
Blog: The New Resource Groups Tagging API Makes It Easier to Programmatically Manage Tags on Resources Across AWS Services:
https://aws.amazon.com/about-aws/whats-new/2017/03/the-new-resource-groups-tagging-api-makes-it-easier-to-programmatically-manage-tags-on-resources-across-aws-services/
