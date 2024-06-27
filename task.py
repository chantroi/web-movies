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

for file in s3.list_objects(Bucket="files")["Contents"]:
    if file["Key"].endswith(".mp4"):
        path = f'videos/{file["Key"]}'
    elif file["Key"].endswith(".jpg"):
        path = f'images/{file["Key"]}'
    elif file["Key"].endswith(".mp3"):
        path = f'music/{file["Key"]}'
    else:
        path = f'texts/{file["Key"]}'
    data = s3.get_object(Bucket="files", Key=file["Key"])["Body"].read()
    fs.put(path, data)
    print(f"Uploaded {file['Key']} to {path}")