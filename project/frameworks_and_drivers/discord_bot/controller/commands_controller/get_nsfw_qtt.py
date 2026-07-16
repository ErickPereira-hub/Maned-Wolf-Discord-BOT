from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Member
from typing import Dict
from requests import Response, get
from time import time
import os
from project.frameworks_and_drivers.discord_bot.view.graphs.channels import ChannelsGraph
from project.frameworks_and_drivers.discord_bot.view.embed_middleware import get_emb_without_author
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.command()
async def get_nsfw_qtt(ctx: commands.Context, chart = "no"):

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
    URL: str = os.getenv("BASE_URL") + f"/channel/analysis?server_id={server_id}&member_id={author.id}"
    resp: Response = get(URL)
    status: int = resp.status_code
    CacheBacklog.update_backlog(status)#<---Updating the backlog in RAM

    if status != 200:

        if resp.status_code == 404:
            return

        if status == 429:
            await ctx.reply(f"❌ Too many requests. Hold on, please!")
            return

        await ctx.reply(f"❌ problem during a request to the API\nStatus code: {status}")
        return

    #Catching the data
    data: Dict[str, Dict[str, int]] = resp.json()["data"]

    nsfw_yes_ch_qtt: int = data["yes"]
    nsfw_no_ch_qtt: int = data["no"]
    tot_qtt: int = nsfw_yes_ch_qtt + nsfw_no_ch_qtt

    if chart != "chart":

        t_end: float = time()
        t_interval: int = t_end - t_start

        MSG: str = f"""
        🔗 NSFW information:
        NSFW channel count: {nsfw_yes_ch_qtt} ( {(100 * nsfw_yes_ch_qtt / tot_qtt):.2f} % )
        Non-NSFW channel count: {nsfw_no_ch_qtt} ( {(100 * nsfw_no_ch_qtt / tot_qtt):.2f} % )\n
        Backend Latency: {(1000 * t_interval):.0f} ms
        """

        await ctx.reply(MSG)
        return
    
    ChannelsGraph.build_nsfw_pie(
        yes_ch_qtt = nsfw_yes_ch_qtt,
        no_ch_qtt = nsfw_no_ch_qtt,
        server_id = server.id,
        author_id = author.id
    )

    #Taking the time
    t_end: float = time()
    t_interval: float = t_end - t_start
    
    #Capturing the view with the image, delivering it to discord and deleting the image
    IMG_PATH: str = ChannelsGraph.REPO_PATH + f"/channels_nsfw_{server.id}{author.id}.png"
    emb, file = get_emb_without_author(
        title = "Quantity of NSFW and non-NSFW channels",
        desc = f"",
        footer_txt = f"Backend Latency: {(1000 * t_interval):.2f} ms",
        img_path = IMG_PATH
    )

    await ctx.reply(embed = emb, file = file)
    os.remove(IMG_PATH) #<--- Deletes the image