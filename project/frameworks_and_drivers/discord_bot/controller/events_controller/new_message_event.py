from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord import Message
from typing import Dict
import os
from requests import Response, post
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_message(msg: Message):

    if msg.author.bot: #<--- The author is the bot
        return #Ignoring the event for bot messages

    if msg.guild is None: #<--- Message was sent to DM, not in the server
        return #Ignoring the event for DM messages
    
    message_data: Dict[str, int | str] = {
        "msg_id": msg.id,
        "msg_text": msg.content,
        "msg_date": str(msg.created_at) if msg.created_at is not None else None,
        "msg_edited_at": str(msg.edited_at) if msg.edited_at is not None else None,
        "author_id": msg.author.id,
        "channel_id": msg.channel.id,
        "server_id": msg.guild.id,
        "mname" : msg.author.global_name,
        "mcategory" : "bot" if msg.author.bot else "human",
        "mjoined_at" : str(msg.author.joined_at) if msg.author.joined_at is not None else None,
        "maccount_create_at" : str(msg.author.created_at),
        "cname" : msg.channel.name,
        "ccategory" : msg.channel.category.name if msg.channel.category is not None else None,
        "cis_nsfw" : "yes" if msg.channel.is_nsfw() else "no"
    }

    #Doing the request
    URL: str = os.getenv("BASE_URL") + "/msg"
    resp: Response = post(URL, json = message_data)
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM

    #If the operation wasn't done
    if resp.status_code != 201:
        print("❌ TROUBLE: the database couldn't capture a massage")

    await MW_BOT.bot.process_commands(msg)