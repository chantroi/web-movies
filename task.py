import os
import boto3
from src.detafs import DetaFs

endpoint = os.environ["S3_URL"]
key = os.environ["S3_KEY"]
secret = os.environ["S3_SECRET"]

fs = DetaFs(os.environ["DETA_KEY"])

s3 = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret).client(
    "s3", endpoint_url=endpoint
)

for file in fs.ls():
    if 'uptime-kuma' in file:
        fs.remove(file)

for file in s3.list_objects(Bucket="storage")["Contents"]:
    try:
        if any(folder in file["Key"] for folder in ["images/", "video/", "music/"]):
            path = file["Key"]
            data = s3.get_object(Bucket="storage", Key=file["Key"])["Body"].read()
            fs.put(path, data)
            print(f"Uploaded {file['Key']} to {path}")
    except Exception as e:
            print(e)