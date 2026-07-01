from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Member
from typing import Tuple, List
from requests import Response, get
from time import time
from project.frameworks_and_drivers.discord_bot.view.get_single_prob_new_msgs_view import SingleProbNewMessagesView
import os
from project.frameworks_and_drivers.discord_bot.view.graphs.graph import Graph
from project.frameworks_and_drivers.discord_bot.view.embed_middleware import get_emb_without_author
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.command()
async def get_prob_new_msg(ctx: commands.Context, from_qtt: int, until_qtt: int, chart: str = "no"):
    
    #Checking the parameters
    if from_qtt < 0 or until_qtt < from_qtt:
        await ctx.reply("❌ INVALID COMMAND: the first and second arguments must be positive numbers and the second argument can't be lower than the first one")
        return
    
    #Checking if we can access the discord server
    server: Guild = ctx.guild
    author: Member = ctx.author
    if server is None or author is None:
        await ctx.reply("❌ Access not allowed due to discord permissions")
        return
    
    t_start: float = time()
    #First contact
    PREP_MSG: str = "🔄 Gathering the data and evaluating the probability . . ."
    await ctx.reply(PREP_MSG)
    
    #Calling the data throughout the API
    URL: str = os.getenv("BASE_URL") + f"/msg/poisson?server_id={server.id}&from={from_qtt}&until={until_qtt}&chart={chart}&member_id={author.id}"
    resp: Response = get(URL)
    status: int = resp.status_code
    CacheBacklog.update_backlog(status)#<---Updating the backlog in RAM

    #If we get into trouble with the API:
    if status != 200:
        
        if status == 429:
            await ctx.reply(f"❌ Too many requests. Hold on, please!")
            return

        if status == 403:
            await ctx.reply(f"⚠️ {resp.json()["message"]}")
            return

        await ctx.reply(f"❌ problem during a request to the API\nProblem Status ---> {status}")
        return

    if chart != "chart":
        data: float = resp.json()["data"]
        await ctx.reply(str(SingleProbNewMessagesView(prob = data, from_qtt = from_qtt, to_qtt = until_qtt)))
        return
    
    data: List[Tuple[int, float]] = resp.json()["data"] #<--- Points of quantities and their Poisson probability
    prob: float = resp.json()["probability"]

    #Building the bar graph
    Graph.build_dist_poisson(
        dataset = data,
        from_qtt = from_qtt,
        until_qtt = until_qtt,
        server_id = server.id,
        author_id = author.id,
        style = "msgs")
    
    #Taking the time
    t_end: float = time()
    t_interval: float = t_end - t_start
    
    #Capturing the view with the image, delivering it to discord and deleting the image
    IMG_PATH: str = Graph.REPO_PATH + f"/msgs_{server.id}{author.id}_poisson.png"
    emb, file = get_emb_without_author(
        title = "Probability distribution for tomorrow's new message count",
        desc = f"Probability of gaining {f"{from_qtt} to {until_qtt}" if from_qtt < until_qtt else from_qtt} new messages on the server tomorrow: {(100 * prob):.3f} %",
        footer_txt = f"Backend Latency: {(1000 * t_interval):.2f} ms",
        img_path = IMG_PATH
    )

    await ctx.reply(embed = emb, file = file)
    os.remove(IMG_PATH) #<--- Deletes the image

@get_prob_new_msg.error
async def error_get_prob_new_members(ctx: commands.Context, ERR: Exception):

    END_MSG: str = """\n
The command has the format: wolf?get_prob_new_msg from_qtt unti_qtt chart, where from_qtt is the starting quantity,
until_qtt is the quantity at the end, chart will show a distribution graph if you write \'chart\' at this place, but this
parameter can be ignored, not showing the figure by default, Both from_qtt and until_qtt must be integers."""

    if isinstance(ERR, commands.MissingRequiredArgument):
        await ctx.reply("❌ INVALID COMMAND: you forgot to define all parameters." + END_MSG)
    elif isinstance(ERR, commands.BadArgument):
        await ctx.reply("❌ INVALID COMMAND: the first and second parameters must be numbers" + END_MSG)