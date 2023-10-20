#! /usr/bin/python3

import requests
import json
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

url = "https://auth.media.jio.com/tokenservice/apis/v1/refreshtoken"

payload = json.dumps({
  "refreshToken": "c1df31fd-4866-4c02-bd8e-508dc9df3696",
  "devicetype": "phone",
  "versionCode": 290,
  "os": "android",
  "appName": "RJIL_JioTV",
  "deviceId": "3c6d6b5702fa09bd"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')