import pyrogram
import deta

deta = deta.Deta("c0kEEGmHJte_YjH9AKDzdmP4tm6Zyge3Fme9KyMRNwXB")
bot = pyrogram.Client(
    "uploader",
    21021245,
    "7b32ea92719781c5e22ede319c5dbde5",
    bot_token="5846865945:AAFdGzRy-1-KZXZOm1je_oR-LQTsCOCHfqI",
)
drive = deta.Drive("files")
bot.start()
for i in range(1, 1672):
    m = bot.get_messages("contentdownload", i)
    if m.video:
        print(i)
        video = bot.download_media(m, in_memory=True)
        name = video.name
        drive.put(name, video.getvalue())
        print(name)
