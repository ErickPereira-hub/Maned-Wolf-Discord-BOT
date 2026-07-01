from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Member, TextChannel
from typing import List, Dict
from requests import Response, get
from time import time
from project.frameworks_and_drivers.discord_bot.view.graphs.members import MembersGraph
import os
from project.frameworks_and_drivers.discord_bot.view.get_top_members import GetTopMembersView
from project.frameworks_and_drivers.discord_bot.view.embed_middleware import get_emb_without_author
from datetime import datetime, timedelta
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.command()
async def get_top_members_on_channel(ctx: commands.Context, chart: str = "no"):
    
    author: Member = ctx.author
    server: Guild = ctx.guild #<--- Capturing the server
    channel: TextChannel = ctx.channel
    if server is None or author is None or channel is None:
        await ctx.reply("❌ Discord didn't allow us to grab recent updates. Try later!")
        return

    #Informing the user that his/her data is being processed    
    MSG_PREP: str = "🔄 Gathering the data . . ."
    await ctx.reply(MSG_PREP)

    t_start: float = time() #<--- Starting point in time

    #Grabbing the last 24 hours datetime
    time_to_past_in_h: int = 24
    from_date: datetime = datetime.utcnow() - timedelta(hours = time_to_past_in_h)

    #Sending a request of data to the API
    URL: str = os.getenv("BASE_URL") + f"/member/top_members?server_id={server.id}&member_id={author.id}&channel_id={channel.id}&from_date={from_date}&by=channel" #<--- channel_id as -1 because we don't need to inform any channel here
    resp: Response = get(URL)
    status: int = resp.status_code
    CacheBacklog.update_backlog(status)#<---Updating the backlog in RAM

    if status != 200:
        
        if status == 429:
            await ctx.reply(f"❌ Wait, too many requests were done in your name.")
            return

        await ctx.reply(f"❌ Bot can't allocate the data from the API\nStatus: {status}")
        return

    data: List[Dict[str, int]] = resp.json() #<--- JSON that comes from the API with data from a database

    if chart != "chart":
        view: GetTopMembersView = GetTopMembersView(
            data = data,
            hours = time_to_past_in_h, #<--- Analysed past window
            option = "channel"
            )
        await ctx.reply(str(view))
        return
    
    #Building the graph
    MembersGraph.build_top_members(
        dataset = data,
        server_id = server.id,
        author_id = author.id,
        option = "channel"
        )
    
    #Path to the image
    IMG_PATH: str = MembersGraph.REPO_PATH + f"/best_members_by_channel_{server.id}{author.id}.png"
    
    #Grabbing the backend latency
    t_end: float = time()
    t_interval: float = t_end - t_start
    
    emb, file = get_emb_without_author(
        title = "Top 5 most active members in this channel",
        desc = f"",
        footer_txt = f"Backend Latency: {(1000 * t_interval):.2f} ms",
        img_path = IMG_PATH
    )

    await ctx.reply(embed = emb, file = file)
    os.remove(IMG_PATH)