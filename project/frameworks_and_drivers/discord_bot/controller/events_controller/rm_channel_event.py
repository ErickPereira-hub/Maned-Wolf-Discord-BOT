from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from requests import Response, delete
import os
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
    id: int = channel.id # <--- Id of the channel that has been deleted
    #Doing the request
    URL: str = os.getenv("BASE_URL") + f"/channel?channel_id={id}"
    resp: Response = delete(URL)
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM

    #Giving information of the ERROR to the log if something bad happens
    if resp.status_code != 200:
        print(f"ERROR ---> CHANNEL OF ID {id} WASN'T DELETED")