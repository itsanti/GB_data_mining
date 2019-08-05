from config import api

proxy = {
    'server': '95.216.224.183',
    'port': 1080,
    'login': '',
    'pass': ''
}

from telethon import TelegramClient
import socks
import re

client = TelegramClient('gbuhw', api.get('id'), api.get('hash'),
                        proxy=(socks.SOCKS5, proxy['server'], proxy['port'], True))

client.start()
dialogs = client.get_dialogs()

#for msg in client.iter_messages(dialogs[0]):
#    print(msg)
client.get_participants(dialogs[0])