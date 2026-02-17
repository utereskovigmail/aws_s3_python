import os
import boto3

#print("Сало - це смачно і дуже корисно!")
s3_client = boto3.client('s3') # S3 client
s3_resource = boto3.resource('s3') # S3 resource

response = s3_client.list_buckets() # List all buckets
for bucket in response['Buckets']:
    print(bucket)

 