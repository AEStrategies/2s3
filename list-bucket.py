#!/usr/bin/env python3

import sys

import boto3

S3_BUCKET_NAME = sys.argv[1]  # BUCKET_FOR_FILE_TRANSFER

s3_resource = boto3.resource("s3")
s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
print('Listing AWS S3 Bucket objects:')
for obj in s3_bucket.objects.all():
    print(f'-- {obj.key}')
