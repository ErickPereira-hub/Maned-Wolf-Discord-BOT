from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from requests import Response, patch
import os
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_guild_channel_update(before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
    #Capturing the data from the edited channel
    channel_id: int = after.id
    new_name: str = after.name
    new_category: str | None = after.category
    new_is_nsfw: str = "yes" if after.is_nsfw() else "no"
    sid: int = after.guild.id
    
    #Sending a request of edition to the database throughout the API
    URL: str = os.getenv("BASE_URL") + f"/channel?channel_id={channel_id}&new_name={new_name}&new_category={new_category}&new_is_nsfw={new_is_nsfw}&server_id={sid}"
    resp: Response = patch(URL)
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM
    
    #if something went bad on the API
    ERR = f"ERROR ---> UPDATE OF CHANNEL WITH ID {channel_id} WENT WRONG"
    if resp.status_code != 200:
        print(ERR)