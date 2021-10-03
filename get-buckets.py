#!/usr/bin/env python

import boto3

resource = boto3.resource("s3")
print("Listing Amazon S3 Buckets:")
for bucket in resource.buckets.all():
    print(f"-- {bucket.name}")
