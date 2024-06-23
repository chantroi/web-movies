import os
import datetime
import pytz
from typing import List
from odetam import DetaModel

vntz = pytz.timezone("Asia/Ho_Chi_minh")


class Note(DetaModel):
    name: str
    created_at: datetime.date = datetime.datetime.now(vntz)
    content: str = ""
    urls: List[str]

    class Config:
        table_name = "notebase"
        deta_key = os.environ["DETA_KEY"]
