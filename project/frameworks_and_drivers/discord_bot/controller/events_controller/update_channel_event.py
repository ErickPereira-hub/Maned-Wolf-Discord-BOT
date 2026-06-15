from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from typing import Dict
from requests import Response, patch
import os

@MW_BOT.bot.event
async def on_guild_channel_update(before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
    #Capturing the data from the edited channel
    channel_id: int = after.id
    new_name: str = after.name
    new_category: str | None = after.category
    new_is_nsfw: str = "yes" if after.is_nsfw() else "no"
    
    #Sending a request of edition to the database throughout the API
    URL: str = os.getenv("BASE_URL") + f"/channel?channel_id={channel_id}&new_name={new_name}&new_category={new_category}&new_is_nsfw={new_is_nsfw}"
    resp: Response = patch(URL)
    
    #if something went bad on the API
    ERR = f"ERROR ---> EDITION OF CHANNEL WITH ID {channel_id} WENT WRONG"
    if resp.status_code != 200:
        print(ERR)