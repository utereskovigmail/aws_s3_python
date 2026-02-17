import os
import boto3

#print("Сало - це смачно і дуже корисно!")
s3_client = boto3.client('s3') # S3 client
s3_resource = boto3.resource('s3') # S3 resource

response = s3_client.list_buckets() # List all buckets
for bucket in response['Buckets']:
    print(bucket)

response = s3_client.list_objects_v2(Bucket='demo-bucket-bober') # List objects in a bucket
objects = response.get('Contents', [])
print(objects)

s3_client.download_file("demo-bucket-bober", "bober.jpg", "downloaded_bober.jpg") 
s3_client.download_file("demo-bucket-bober", "info.txt", "downloaded_info.txt") 