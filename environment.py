import os
import requests

secret_url = os.environ["SECRET"]

response = requests.get(secret_url)
data = response.json()

deta_key = data["deta"]["sm"]
s3_endpoint = data["s3"]["idrive"]["endpoint"]
s3_key = data["s3"]["idrive"]["key"]
s3_secret = data["s3"]["idrive"]["secret"]
bot_token = data["bot"]["tiktokdouyin"]
project_id = os.environ["PROJECT_ID"]
