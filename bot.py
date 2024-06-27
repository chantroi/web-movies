import os
import boto3
from pyrogram import Client, filters
from pyrogram.types import Message
from src.detafs import DetaFs

endpoint = os.environ["S3_URL"]
key = os.environ["S3_KEY"]
secret = os.environ["S3_SECRET"]

bot = Client(
    "bot",
    21021245,
    "7b32ea92719781c5e22ede319c5dbde5",
    bot_token=os.environ["BOT_TOKEN"],
)

fs = DetaFs(os.environ["DETA_KEY"])
s3 = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret).client(
    "s3", endpoint_url=endpoint
)


@bot.on_message(filters.chat("contentdownload") & filters.video)
def download_video(c: Client, m: Message):
    file = c.download_media(m, in_memory=True)
    fs.put("video/" + file.name, file.getvalue())
    s3.upload_fileobj(
        Fileobj=file,
        Bucket="storage",
        Key="video/" + file.name,
        ExtraArgs={"ACL": "public-read", "ContentType": "video/mp4"},
    )
    print(f"Uploaded {file.name} to {file.name}")


bot.run()