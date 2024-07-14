import s3fs
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
s3 = s3fs.S3FileSystem(
    key=s3_key,
    secret=s3_secret,
    endpoint_url=s3_endpoint,
)


def upload_to_s3(file_name, file_data):
    s3_path = f"bosuutap/video/{file_name}"
    with s3.open(s3_path, "wb") as s3_file:
        s3_file.write(file_data)
    s3.setxattr(s3_path, copy_kwargs={"ContentType": "video/mp4"})


@bot.on_message(filters.chat("contentdownload") & filters.video)
def download_video(c: Client, m: Message):
    file = c.download_media(m, in_memory=True)
    fs.put(file.name, file.getvalue())
    upload_to_s3(file.name, file.getvalue())
    print(f"Uploaded {file.name}")


@bot.on_message(filters.command("upload"))
def upload(c: Client, m: Message):
    if m.reply_to_message:
        file = c.download_media(m.reply_to_message, in_memory=True)
        fs.put(file.name, file.getvalue())

        upload_to_s3(file.name, file.getvalue())

        m.reply(f"Uploaded {file.name}", quote=True)
    else:
        m.reply("Reply to a message with /upload", quote=True)


@bot.on_message(filters.command("upload_s3"))
def upload_s3(c: Client, m: Message):
    if m.reply_to_message:
        file = c.download_media(m.reply_to_message, in_memory=True)
        upload_to_s3(file.name, file.getvalue())

        m.reply(f"Uploaded {file.name}", quote=True)
    else:
        m.reply("Reply to a message with /upload_s3", quote=True)


@bot.on_message(filters.command("delete_file"))
def delete_file(c: Client, m: Message):
    if len(m.command) >= 2:
        filename = m.command[1]
        fs.delete(filename)
        m.reply(f"Deleted {filename}", quote=True)
    else:
        m.reply("Provide a filename with /delete_file", quote=True)


print("Bot started")
bot.run()
