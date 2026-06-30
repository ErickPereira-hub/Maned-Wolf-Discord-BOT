from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Member
from typing import Dict
from requests import Response, get
from time import time
import os
from project.frameworks_and_drivers.discord_bot.view.embed_middleware import get_emb_without_author
from project.frameworks_and_drivers.discord_bot.view.graphs.channels import ChannelsGraph
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.command()
async def get_cat_qtt(ctx: commands.Context, chart: str = "no"):

    server: Guild | None = ctx.guild
    author: Member | None = ctx.author

    if server is None or author is None:
        await ctx.reply("❌ Access not allowed due to discord permissions")
        return
    
    server_id: int = server.id #<--- Server id to access data from this server, nothing else
    t_start: float = time()

    #First contact
    PREP_MSG: str = "🔄 processing the data from the channels . . ."
    await ctx.reply(PREP_MSG)

    #Calling the data throughout the API
    URL: str = os.getenv("BASE_URL") + f"/channel/analysis?server_id={server_id}&style=category&member_id={author.id}"
    resp: Response = get(URL)
    status: int = resp.status_code
    CacheBacklog.update_backlog(status)#<---Updating the backlog in RAM

    if status != 200:

        if status == 429:
            await ctx.reply(f"❌ Too many requests. Hold on, please!")
            return

        await ctx.reply(f"❌ problem during a request to the API\nStatus code: {status}")
        return

    #Catching the data
    data: Dict[str, Dict[str, int]] = resp.json()["data"]
    txt_ch_qtt: int = data["Text channels"]
    voice_ch_qtt: int = data["Voice channels"]
    tot_qtt: int = txt_ch_qtt + voice_ch_qtt

    if chart != "chart":

        t_end: float = time()
        t_interval: int = t_end - t_start

        MSG: str = f"""
        🔗 Category information:
        Quantity of channels (text and voice channels): {tot_qtt}\n
        Quantity of voice channels: {voice_ch_qtt} ( {(100 * voice_ch_qtt / tot_qtt):.2f} % )
        Quantity of text channels: {txt_ch_qtt} ( {(100 * txt_ch_qtt / tot_qtt):.2f} % )\n
        Backend Latency: {(1000 * t_interval):.0f} ms
        """

        await ctx.reply(MSG)
        return
    
    ChannelsGraph.build_cat_pie(
        txt_ch_qtt = txt_ch_qtt,
        voice_ch_qtt = voice_ch_qtt,
        server_id = server.id,
        author_id = author.id
    )

    #Taking the time
    t_end: float = time()
    t_interval: float = t_end - t_start
    
    #Capturing the view with the image, delivering it to discord and deleting the image
    IMG_PATH: str = ChannelsGraph.REPO_PATH + f"/channels_cat_{server.id}{author.id}.png"
    emb, file = get_emb_without_author(
        title = "Quantities of channels by category",
        desc = f"",
        footer_txt = f"Backend Latency: {(1000 * t_interval):.2f} ms",
        img_path = IMG_PATH
    )

    await ctx.reply(embed = emb, file = file)
    os.remove(IMG_PATH) #<--- Deletes the image