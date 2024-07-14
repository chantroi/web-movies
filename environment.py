import os
import requests

if os.environ.get("SECRET"):
    secret_url = os.environ["SECRET"]
    response = requests.get(secret_url, timeout=5)
    data = response.json()
    deta_key = data["deta"]["sm"]
    s3_endpoint = data["s3"]["idrive"]["endpoint"]
    s3_key = data["s3"]["idrive"]["key"]
    s3_secret = data["s3"]["idrive"]["secret"]
    bot_token = data["bot"]["tiktokdouyin"]
if os.environ.get("DETA_PROJECT_KEY"):
    DETA_PROJECT_KEY = os.environ["DETA_PROJECT_KEY"]
    deta_key = os.getenv("DETA_KEY", DETA_PROJECT_KEY)
