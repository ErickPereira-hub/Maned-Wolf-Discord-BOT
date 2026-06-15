from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord import Message
from typing import Dict
import os
from requests import Response, post

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
        "server_id": msg.guild.id
    }

    #Doing the request
    URL: str = os.getenv("BASE_URL") + "/msg"
    resp: Response = post(URL, json = message_data)

    #If the operation wasn't done
    if resp.status_code != 201:
        await msg.author.send("❌ TROUBLE: the database couldn't capture your massage")