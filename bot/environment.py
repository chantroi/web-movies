import os
import requests

secret_url = os.environ["SECRET"]
response = requests.get(secret_url, timeout=5)
data = response.json()
deta_key = data["access"]["deta"]["sm"]
s3_endpoint = data["s3"][4]["endpoint"]
s3_key = data["s3"][4]["key"]
s3_secret = data["s3"][4]["secret"]
bot_token = data["access"]["telegram"]["td"]
