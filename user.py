
from data import api_id, api_hash
from telethon import TelegramClient
from telethon.sessions import StringSession

print("working")
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())