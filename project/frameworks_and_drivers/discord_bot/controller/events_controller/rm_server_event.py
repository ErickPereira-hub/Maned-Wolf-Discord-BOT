from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from requests import Response, delete
import os
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_guild_remove(guild: discord.Guild):

    owner: discord.Member = guild.owner #<--- Owner of the server

    if owner is None:
        return #<--- Stop the operation due to a problem
    
    await owner.send("🔄 Deleting your server's data from our database . . .")

    server_id: int = guild.id

    #Doing a delete request
    URL: str = os.getenv("BASE_URL") + f"/server?server_id={server_id}"
    resp: Response = delete(URL) #<--- Requesting a deletion to the API
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM

    #If something bad happens
    if resp.status_code != 200:
        await owner.send("❌ Couldn't do the deletion operation properly")
        return
    
    await owner.send("✅ Deletion operation completed. I don't have your data anymore!")