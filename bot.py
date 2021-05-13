import discord
from dotenv import load_dotenv
import sys
import os
import time

from tduwb import main


load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    campus_list = [
        {
            "name": "東京千住",
            "area_code": 130000,
            "channel_id": os.environ["SENJU_CHANNEL_ID"],
            "jma_link": "https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code=1312100",
        },
        {
            "name": "埼玉鳩山",
            "area_code": 110000,
            "channel_id": os.environ["HATOYAMA_CHANNEL_ID"],
            "jma_link": "https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code=1134800",
        },
    ]
    for campus in campus_list:
        fcast = main.MainText(
            camplus_name=campus["name"],
            area_code=campus["area_code"],
            jma_link=campus["jma_link"],
        )

        print(fcast.main_text())
        print(fcast.week_forecast())

        channel_id = campus["channel_id"]
        channel = client.get_channel(int(channel_id))
        await channel.send(fcast.main_text())
        await channel.edit(topic=fcast.week_forecast())

    # sleep入れないとherokuでおかしくなる
    time.sleep(5)
    sys.exit()


client.run(os.environ["DISCORD_TOKEN"])