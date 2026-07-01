from discord.ext import tasks
from requests import Response, get
from typing import List
from discord import Guild, User, Forbidden
from datetime import datetime, timedelta
import os
from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT

@tasks.loop(hours = 24)
async def send_msg_to_most_active_member():

    servers: List[Guild] = list(MW_BOT.bot.guilds) #<--- List of all servers
    since: datetime = str(datetime.utcnow() - timedelta(hours = 24))

    for server in servers:
        #Requesting the most active member inside the database for the server
        URL: str = os.getenv("BASE_URL") + f"/member/most_active_member?server_id={server.id}&from_date={since}"
        resp: Response = get(URL)
        data: int = resp.json()['id']

        if data == -1: #<---  -1 for data means that we don't have a most active member because the last day hasn't comments in any channel of the server (very commom in small servers)
            continue

        member: User = await MW_BOT.bot.fetch_user(data)

        #Sending the message to the most active member
        try:
            await member.send(f"🎉 Congratulations. You were the most active member inside {server.name} for the last 24 hours")
        except Forbidden: pass #<--- If the user has blocked the bot, this exception will happen, so we just ignore.