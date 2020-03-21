import requests
import base64

import supersecret

API_ENDPOINT = 'https://discordapp.com/api/v6'
CLIENT_ID = supersecret.getSecret('discord_bot_ctfbot', 'client_id')
CLIENT_SECRET = supersecret.getSecret('discord_bot_ctfbot', 'client_secret')

def get_token():
  data = {
    'grant_type': 'client_credentials',
    'scope': 'identify connections bot'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  r.raise_for_status()
  return r.json()

print(get_token())
