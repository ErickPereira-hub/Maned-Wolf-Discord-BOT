from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild
from typing import Dict
from requests import Response, get
from time import time
import os

@MW_BOT.bot.command()
async def get_cat_qtt(ctx: commands.Context):

    server: Guild | None = ctx.guild

    if server is None:
        await ctx.reply("❌ Access not allowed due to discord permissions")
        return
    
    server_id: int = server.id #<--- Server id to access data from this server, nothing else
    t_start: float = time()

    #First contact
    PREP_MSG: str = "🔄 processing the data from the channels . . ."
    await ctx.reply(PREP_MSG)

    #Calling the data throughout the API
    URL: str = os.getenv("BASE_URL") + f"/channel/analysis?server_id={server_id}&style=category"
    resp: Response = get(URL)
    status: int = resp.status_code

    if status != 200:
        await ctx.reply(f"❌ problem during a request to the API\nStatus code: {status}")
        return
    
    #Catching the data
    data: Dict[str, Dict[str, int]] = resp.json()["data"]
    txt_ch_qtt: int = data["Text channels"]
    voice_ch_qtt: int = data["Voice channels"]
    tot_qtt: int = txt_ch_qtt + voice_ch_qtt

    t_end: float = time()
    t_interval: int = t_end - t_start

    MSG: str = f"""
    🔗 Category information:
    Quantity of channels (text and voice channels): {tot_qtt}\n
    Quantity of voice channels: {voice_ch_qtt} ( {(100 * voice_ch_qtt / tot_qtt):.2f} % )
    Quantity of text channels: {txt_ch_qtt} ( {(100 * txt_ch_qtt / tot_qtt):.2f} % )\n
    Backend Latency: {(1000 * t_interval):.0f} sec
    """

    await ctx.reply(MSG)