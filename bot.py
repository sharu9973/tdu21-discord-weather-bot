import discord
from dotenv import load_dotenv
import sys
import os
import time

import main

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    campus_list = [
        {"name": "東京千住", "area_code": 130000, "channel_id": 833498626747138098},
        {"name": "埼玉鳩山", "area_code": 110000, "channel_id": 833498587992293386},
    ]

    for campus in campus_list:

        text = main.main(**campus)

        channel_id = campus["channel_id"]
        channel = client.get_channel(int(channel_id))
        await channel.send(text)
    # sleep入れないとherokuでおかしくなる
    time.sleep(5)
    sys.exit()


client.run(os.environ["DISCORD_TOKEN"])