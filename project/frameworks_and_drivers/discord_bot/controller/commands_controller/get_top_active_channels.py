from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Member
from typing import List, Dict
from requests import Response, get
from time import time
from project.frameworks_and_drivers.discord_bot.view.get_top_active_channels_view import GetTopActiveChannelsView
import os
from project.frameworks_and_drivers.discord_bot.view.embed_middleware import get_emb_without_author
from project.frameworks_and_drivers.discord_bot.view.graphs.channels import ChannelsGraph
from project.application.utils.max_str_size import get_max_str_size

@MW_BOT.bot.command()
async def get_top_active_channels(ctx: commands.Context, show: str = "no"):

    #Checking if discord can catch the server
    server: Guild = ctx.guild
    author: Member = ctx.author
    if server is None or author is None:
        await ctx.reply("❌ Access not allowed due to discord permissions")
        return

    t_start: float = time()
    #Message informing that the application is preparing stuff
    MSG_PREP: str = "🔄 grabbing the data . . ."
    await ctx.reply(MSG_PREP)

    #Sending a request of data to the API
    URL: str = os.getenv("BASE_URL") + f"/top_active_ch?server_id={server.id}"
    resp: Response = get(URL)
    status: int = resp.status_code

    #Problem during the request must exit the endpoint
    if status != 200:
        await ctx.reply(f"❌ problem during a request to the API\nStatus: {status}")
        return
    
    data: List[Dict[str, int]] = resp.json()["data"]

    if show != "show":
        view: str = GetTopActiveChannelsView(data)
        await ctx.reply(view)
        return

    #Organizing the data of the best channels
    ch_names: List[str] = [get_max_str_size(list(chd.keys())[0], max_s = 6) for chd in data]
    msg_volume: List[int] = [list(chd.values())[0] for chd in data]
    
    #Building the graph
    ChannelsGraph.build_top_ch_bars(
        ch_names = ch_names,
        msg_volume_per_channel = msg_volume,
        server_id = server.id,
        author_id = author.id
        )
    
    #Path to the image
    IMG_PATH: str = ChannelsGraph.REPO_PATH + f"/top_ch_{server.id}{author.id}.png"
    
    #Grabbing the backend latency
    t_end: float = time()
    t_interval: float = t_end - t_start
    
    emb, file = get_emb_without_author(
        title = "Volumes of messages for the most active channels",
        desc = f"",
        footer_txt = f"Backend Latency: {(100 * t_interval):.2f} ms",
        img_path = IMG_PATH
    )

    await ctx.reply(embed = emb, file = file)
    os.remove(IMG_PATH)