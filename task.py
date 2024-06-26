import os
from src.detafs import DetaFs
from src.detafs.core import DetaFs
from s3fs import S3FileSystem

endpoint = os.environ["S3_URL"]
key = os.environ["S3_KEY"]
secret = os.environ["S3_SECRET"]

fs = DetaFs(os.environ["DETA_KEY"])
s3 = S3FileSystem(endpoint_url=endpoint, key=key, secret=secret)

for filename in fs.ls():
    if filename.endswith(".mp4"):
        with s3.open(f"storage/video/{filename}", "wb") as f:
            data = fs.open(filename).read()
            f.write(data)
    if filename.endswith(".mp3"):
        with s3.open(f"storage/music/{filename}", "wb") as f:
            data = fs.open(filename).read()
            f.write(data)

    elif any(filename.endswith(ext) for ext in [".jpg", ".png", ".gif"]):
        with s3.open(f"storage/image/{filename}", "wb") as f:
            data = fs.open(filename).read()
            f.write(data)
    print(f"File {filename} uploaded to S3.")


print("Files uploaded successfully!")
