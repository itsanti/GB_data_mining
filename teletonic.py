from config import api
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
import socks
import re
import json
from pymongo import MongoClient
from time import sleep

CLIENT = MongoClient('192.168.0.202', 27017)
COLLECTION = CLIENT.ico.tg_groups

proxy = {
    'server': '95.216.224.183',
    'port': 1080,
    'login': '',
    'pass': ''
}

with open('icorating_links.json', 'r') as f:
    icorating_links = json.load(f)

tg_links_icorating = []
for chat in icorating_links:
    name = chat.get('name')
    links = chat.get('socials')
    for link in links:
        if re.findall(r't\.me', link):
            tg_links_icorating.append({'name': name, 'link': link})

client = TelegramClient('gbuhw', api.get('id'), api.get('hash'),
                        proxy=(socks.SOCKS5, proxy['server'], proxy['port'], True))
client.start()

for cur_channel in tg_links_icorating[:5]:
    try:
        channel = client.get_entity(cur_channel.get('link'))
        result = client(JoinChannelRequest(channel))
        channel_name = result.chats[0].username
        print(f'process "{channel_name}" channel. ', end="")

        count = -1
        for u in client.iter_participants(channel_name, aggressive=True):
            #print(u.id, u.first_name, u.last_name, u.username)
            count += 1
            pass

        print(f'users count: {count}')

        data = {
            'name': channel_name,
            'count': count
        }

        _ = COLLECTION.insert_one(data)

        result = client(LeaveChannelRequest(channel))

        sleep(5)
    except ValueError as e:
        print(f'Username Not Occupied: {cur_channel.get("link")}')
        continue
