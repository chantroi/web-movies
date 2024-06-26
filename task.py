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


for filename in fs.ls():
    if filename.endswith(".mp4"):
        data = fs.open(filename).read()
        s3.upload_fileobj(
            data, "storage", f"video/{filename}", ExtraArgs={"ContentType": "video/mp4"}
        )
    if filename.endswith(".mp3"):
        data = fs.open(filename).read()
        s3.upload_fileobj(
            data,
            "storage",
            f"audio/{filename}",
            ExtraArgs={"ContentType": "audio/mpeg"},
        )

    elif any(filename.endswith(ext) for ext in [".jpg", ".png"]):
        data = fs.open(filename).read()
        s3.upload_fileobj(
            data,
            "storage",
            f"images/{filename}",
            ExtraArgs={"ContentType": "image/jpeg"},
        )

    print(f"File {filename} uploaded to S3.")


print("Files uploaded successfully!")
