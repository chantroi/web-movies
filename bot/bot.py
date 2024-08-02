from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from util import Storage
from environment import bot_token

bot = Client(
    "bot",
    21021245,
    "7b32ea92719781c5e22ede319c5dbde5",
    bot_token=bot_token,
)
fs = Storage()


@bot.on_message(filters.command("start"))
async def play_video(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    buttons = [
        [
            InlineKeyboardButton(
                "Web Music",
                url="https://t.me/tiktokanddouyin_bot/music",
            ),
            InlineKeyboardButton(
                "Web Movies", url="https://t.me/tiktokanddouyin_bot/movies"
            ),
        ],
        [InlineKeyboardButton("Douyin", url="https://t.me/tiktokanddouyin_bot/douyin")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await m.reply(
        "TikTok and Douyin Bot",
        reply_markup=reply_markup,
    )


@bot.on_message(filters.chat("contentdownload") & filters.video)
def download_video(c: Client, m: Message):
    file = c.download_media(m, in_memory=True)
    fs.upload(file.name, file.getvalue())
    print(f"Uploaded {file.name}")


@bot.on_message(filters.command("upload"))
def upload(c: Client, m: Message):
    if m.reply_to_message:
        file = c.download_media(m.reply_to_message, in_memory=True)
        if m.video:
            m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            content_type = "video/mp4"
        elif m.photo:
            m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            content_type = "image/jpeg"
        elif m.audio:
            m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            content_type = "audio/mpeg"
        else:
            m.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
            content_type = "application/octet-stream"
        fs.upload(file.name, file.getvalue(), content_type=content_type)
        m.reply(f"Uploaded {file.name}", quote=True)
    else:
        m.reply("Reply to a message with /upload", quote=True)


@bot.on_message(filters.command("upload_s3"))
def upload_s3(c: Client, m: Message):
    if m.reply_to_message:
        file = c.download_media(m.reply_to_message, in_memory=True)
        if m.video:
            m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            content_type = "video/mp4"
        elif m.photo:
            m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            content_type = "image/jpeg"
        elif m.audio:
            m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            content_type = "audio/mpeg"
        else:
            m.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
            content_type = "application/octet-stream"
        fs.upload_to_s3(file.name, file.getvalue(), content_type=content_type)

        m.reply(f"Uploaded {file.name}", quote=True)
    else:
        m.reply("Reply to a message with /upload_s3", quote=True)


@bot.on_message(filters.command("delete_file"))
def delete_file(c: Client, m: Message):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) >= 2:
        filename = m.command[1]
        fs.delete(filename)
        m.reply(f"Deleted {filename}", quote=True)
    else:
        m.reply("Provide a filename with /delete_file", quote=True)


@bot.on_message(filters.command("delete_deta"))
def delete_deta(c: Client, m: Message):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) >= 2:
        filename = m.command[1]
        fs.delete_from_deta(filename)
        m.reply(f"Deleted {filename} from Deta", quote=True)
    else:
        m.reply("Provide a filename with /delete_deta", quote=True)


print("Bot started")
bot.run()
