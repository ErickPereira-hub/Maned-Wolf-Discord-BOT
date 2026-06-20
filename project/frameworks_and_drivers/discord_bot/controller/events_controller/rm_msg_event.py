from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from requests import Response, delete
import os

@MW_BOT.bot.event
async def on_raw_message_delete(payload: discord.RawBulkMessageDeleteEvent):
    id: int = payload.message_id
    #Doing the request
    URL: str = os.getenv("BASE_URL") + f"/msg?msg_id={id}"
    resp: Response = delete(URL)
    #Giving information of the ERROR to the log if something bad happens
    if resp.status_code != 200:
        print(f"ERROR ---> MESSAGE OF ID {id} WASN'T DELETED")