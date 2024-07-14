import boto3
import deta
from pyrogram import Client, filters
from pyrogram.types import Message
from environment import deta_key, s3_endpoint, s3_key, s3_secret, bot_token

bot = Client(
    "bot",
    21021245,
    "7b32ea92719781c5e22ede319c5dbde5",
    bot_token=bot_token,
)

fs = deta.Deta(deta_key).Drive("files")
s3 = boto3.client(
    "s3",
    endpoint_url=s3_endpoint,
    aws_access_key_id=s3_key,
    aws_secret_access_key=s3_secret,
)


@bot.on_message(filters.chat("contentdownload") & filters.video)
def download_video(c: Client, m: Message):
    file = c.download_media(m, in_memory=True)
    fs.put(file.name, file.getvalue())
    s3.upload_fileobj(
        Fileobj=file,
        Bucket="bosuutap",
        Key="video/" + file.name,
        ExtraArgs={"ACL": "public-read", "ContentType": "video/mp4"},
    )
    print(f"Uploaded {file.name} to {file.name}")


@bot.on_message(filters.command("upload"))
def upload(c: Client, m: Message):
    if m.reply_to_message:
        file = c.download_media(m.reply_to_message, in_memory=True)
        fs.put(file.name, file.getvalue())
        s3.upload_fileobj(
            Fileobj=file,
            Bucket="bosuutap",
            Key="video/" + file.name,
            ExtraArgs={"ACL": "public-read", "ContentType": "video/mp4"},
        )
        m.reply(f"Uploaded {file.name}", quote=True)
    else:
        m.reply("Reply to a message with /upload", quote=True)


print("Bot started")
bot.run()
