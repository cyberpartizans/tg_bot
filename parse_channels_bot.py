import telebot
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from threading import Thread, Lock
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
import asyncio

offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 0

client_name = ""
api_id = 0
api_hash = ""
phone_number = ""

with open("config.txt") as reader:
    lines = reader.readlines()
    client_name = lines[0][:-1]
    api_id = int(lines[1][:-1])
    api_hash = lines[2][:-1]
    phone_number = lines[3][:-1]

client = TelegramClient(client_name, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    try:
        client.sign_in(phone_number, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))

async def find_messages():
    global offset_id
    global total_messages
    global limit
    global all_messages
    global total_count_limit
    black_book = await client.get_entity("t.me/BlackBookBelarus")
    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=black_book,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        print(f"Add new messages with len = {len(messages)}")
        for message in messages:
            print(message)
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)

with client:
    client.loop.run_until_complete(find_messages())
