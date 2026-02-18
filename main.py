import os
import boto3
import threading


s3_client = boto3.client('s3') # S3 client
s3_resource = boto3.resource('s3') # S3 resource

response = s3_client.list_buckets() # List all buckets
for bucket in response['Buckets']:
    print(bucket)

# response = s3_client.list_objects_v2(Bucket='demo-bucket-bober') # List objects in a bucket
# objects = response.get('Contents', [])
# print(objects)

# s3_client.download_file("demo-bucket-bober", "bober.jpg", "downloaded_bober.jpg") 
# s3_client.download_file("demo-bucket-bober", "info.txt", "downloaded_info.txt") 

bucket_name = "demo-bucket-bober"
s3_client.put_bucket_versioning(
    Bucket=bucket_name, 
    VersioningConfiguration={'Status': 'Enabled'}
) # Enable versioning on a bucket

# response = s3_client.list_object_versions(
#     Bucket='demo-bucket-bober',
#     Prefix='info.txt'
# ) # List object versions in a bucket

# for version in response.get('Versions'):
#     print(version)

import subprocess
import datetime

def backup_postgres():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.sql"

    password = os.environ.get("DB_PASSWORD")
    
    command = [
        "docker", "exec",
        "-e", f"PGPASSWORD={password}",
        "postgres_db",
        "pg_dump",
        "-U", "ivan",
        "mydb"
    ]

    with open(filename, "w") as f:
        subprocess.run(command, stdout=f)

    print(f"Backup saved to {filename}")

    s3_client.upload_file(
        filename,   # local file
        bucket_name,           # bucket name
        f"backups/{filename}"  # key (path inside bucket)
    )

    print("Upload to s3 complete")



backup_postgres()
