import os
import boto3
import threading
import subprocess
import datetime
import time

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



def backup_postgres():
    print("database backup started")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.sql"
    filepath = os.path.join("backups", filename)

    password = os.environ.get("DB_PASSWORD")
    
    command = [
        "docker", "exec",
        "-e", f"PGPASSWORD={password}",
        "postgres_db",
        "pg_dump",
        "-U", "ivan",
        "mydb"
    ]

    with open(filepath, "w") as f:
        subprocess.run(command, stdout=f)

    print(f"Backup saved to {filepath}")

    s3_client.upload_file(
        filename,   # local file
        bucket_name,           # bucket name
        f"backups/{filename}"  # key (path inside bucket)
    )

    print("Upload to s3 complete")



while True:
    backup_postgres()
    time.sleep(60)
