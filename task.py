import os
import s3fs
import deta
from environment import s3_endpoint, s3_key, s3_secret, deta_key

fs = deta.Deta(deta_key).Drive("files")
s3 = s3fs.S3FileSystem(
    key=s3_key, secret=s3_secret, client_kwargs={"endpoint_url": s3_endpoint}
)
print(s3.ls("storage/video"))
for file in s3.ls("storage/video"):
    with s3.open(file, "rb") as f:
        data = f.read()
    name = file.split("/", 1)[1]
    fs.put(name, data, content_type="video/mp4")
    print(f"Uploaded {name} to {name}")

print("Upload completed")
