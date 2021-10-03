#!/usr/bin/env python

import json

import boto3

client = boto3.client('sts')
response = client.get_caller_identity()
output = {
    'UserId': response['UserId'],
    'Account': response['Account'],
    'Arn': response['Arn']
}

print(json.dumps(output, indent=4))
