from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from requests import Response, delete
import os
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_member_remove(member: discord.Member):
    id: int = member.id
    server_id: int = member.guild.id
    #Doing the request
    URL: str = os.getenv("BASE_URL") + f"/member?member_id={id}&server_id={server_id}"
    resp: Response = delete(URL)
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM

    #Giving information of the ERROR to the log if something bad happens
    if resp.status_code != 200:
        print(f"ERROR ---> MESSAGE OF ID {id} WASN'T DELETED")