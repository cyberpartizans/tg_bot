import telebot
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from threading import Thread, Lock
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
import asyncio
import json

from ner_analyze import analyze_message

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
client.start(phone_number)
print("Client Created")

all_messages = []

@client.on(events.NewMessage)
async def listen_new_messages(event):
    global all_messages
    chat = await event.get_input_chat()
    entity = await client.get_entity(chat)
    print(str(type(entity)))
    if str(type(entity)) == "<class 'telethon.tl.types.Channel'>":
        all_messages.append(event.message)

async def collect_messages_from_channel(limit: int, offset: int, 
    client: TelegramClient, telegram_channel):
    global all_messages 
    channel = await client.get_entity(telegram_channel)
    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset,
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
        for message in messages:
            all_messages.append(message)
        offset = messages[len(messages) - 1].id

async def save_media(messages: list, client: TelegramClient, path: str, prefix: str = "image", limit: int = -1):
    for i, message in enumerate(messages):
        if limit != -1 and i < limit:
            await client.download_media(message, f"{path}/{prefix}_{i}")

def save_messages_json(messages: list, path: str):
    result_dict = {}

    for message in messages:
        if "message" in message.to_dict().keys():
            if len(result_dict) == 0:
                result_dict.update(analyze_message(message.message))
            else:
                analyzed_keywords = analyze_message(message.message)
                for key in analyzed_keywords.keys():
                    if type(result_dict[key]) != list:
                        key_list = []
                        key_list.append(result_dict[key])
                        result_dict[key] = key_list
                    result_dict[key].append(analyzed_keywords[key])

    with open(path, "w") as writer:
        json.dump(result_dict, writer)

with client:
    client.loop.run_until_complete(collect_messages_from_channel(100, 0, client, "t.me/BlackBookBelarus"))
    client.loop.run_until_complete(save_media(all_messages, client, "tmp", limit = 10))
    save_messages_json(all_messages, "test.json")
    client.run_until_disconnected()
