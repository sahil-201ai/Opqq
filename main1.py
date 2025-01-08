import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle

GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SELF_MUTE = os.getenv("SELF_MUTE")
SELF_DEAF = os.getenv("SELF_DEAF")

usertoken1 = os.getenv("TOKEN1")
usertoken2 = os.getenv("TOKEN2")

if not usertoken1 or not usertoken2:
    print("[ERROR] Please add both tokens inside Secrets.")
    sys.exit()

def validate_token(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
    return validate.status_code == 200

if not validate_token(usertoken1) or not validate_token(usertoken2):
    print("[ERROR] One or both of the tokens might be invalid. Please check them again.")
    sys.exit()

# Retrieve user info for both tokens
def get_user_info(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    return requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()

user_info_1 = get_user_info(usertoken1)
user_info_2 = get_user_info(usertoken2)

def joiner(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {"op": 2, "d": {"token": token, "properties": {"$os": "Windows 10", "$browser": "Google Chrome", "$device": "Windows"}, "presence": {"status": status, "afk": False}}, "s": None, "t": None}
    vc = {"op": 4, "d": {"guild_id": GUILD_ID, "channel_id": CHANNEL_ID, "self_mute": SELF_MUTE, "self_deaf": SELF_DEAF}}
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

def run_joiner():
    os.system("clear")
    
    print(f"Logged in as {user_info_1['username']}#{user_info_1['discriminator']} ({user_info_1['id']}).")
    print(f"Logged in as {user_info_2['username']}#{user_info_2['discriminator']} ({user_info_2['id']}).")

    while True:
        joiner(usertoken1, status)
        joiner(usertoken2, status)
        time.sleep(30)

keep_alive()
run_joiner()


