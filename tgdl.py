import os
from pyrogram import Client
from src.detafs import DetaFs

app = Client(
    "tgdl",
    21021245,
    "7b32ea92719781c5e22ede319c5dbde5",
    bot_token=os.environ["BOT_TOKEN"],
)
fs = DetaFs(os.environ["DETA_KEY"])

with app:
    for i in range(0, 908):
        try:
            m = app.get_messages("contentdownload", i)
            if not m:
                raise
            media = app.download_media(m, in_memory=True)
            filename = media.name
            data = media.getvalue()
            fs.put(filename, data)
            print(filename, " saved")
            app.send_message(5665225938, filename + " Saved")
        except Exception as e:
            print(e)
            continue
