from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from typing import Dict
import os
from requests import Response, post
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    ERR_MSG: str = f"ERROR ---> CAN'T INSERT THE CHANNEL {channel.name} TO THE DATABASE"

    channel_data: Dict[str, str | None | int] = {
        "channel_id" : channel.id,
        "channel_name" : channel.name,
        "category" : channel.category.name if channel.category is not None else None,
        "is_nsfw" : "yes" if channel.is_nsfw() else "no",
        "server_id" : channel.guild.id
    }

    #Doing the request
    URL: str = os.getenv("BASE_URL") + "/channel"
    resp: Response = post(URL, json = channel_data)
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM

    #If the operation wasn't done
    if resp.status_code != 201:
        if isinstance(channel, discord.TextChannel):
            try:
                await channel.send("❌ TROUBLE: Our family of maned wolfs couldn't get your data : ^ ( ")
            except discord.Forbidden:
                print(ERR_MSG + " :: NOT ALLOWED BY DISCORD")
            else:
                print(ERR_MSG)
        else:
            print(ERR_MSG)
        return

    #When the response status is 201, the operation has been completed, so we return a good message to that channel
    try:
        if isinstance(channel, discord.TextChannel):
            await channel.send("This channel activity is currently being tracked by our family of named wolfs!")
    except discord.Forbidden:
        pass