from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from typing import Dict
from requests import Response, patch
import os

@MW_BOT.bot.event
async def on_raw_message_edit(payload: discord.RawMessageUpdateEvent):
    #Capturing the data from the edited message
    msg_id: int = payload.message_id
    new_msg_txt: str = payload.data.get("content")
    
    #Sending a request of edition to the database throughout the API
    URL: str = os.getenv("BASE_URL") + f"/msg?msg_id={msg_id}&msg_new_txt={new_msg_txt}"
    resp: Response = patch(URL)
    
    #if something went bad on the API
    ERR = f"ERROR ---> EDITION OF MESSAGE WITH ID {msg_id} WENT WRONG"
    if resp.status_code != 200:
        print(ERR)