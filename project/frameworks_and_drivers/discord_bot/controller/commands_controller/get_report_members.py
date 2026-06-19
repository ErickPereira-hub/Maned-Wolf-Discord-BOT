from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Embed
from typing import Dict, Any, Tuple
import os
from requests import Response, get
from project.frameworks_and_drivers.discord_bot.view.graphs.members import MembersGraph
from project.frameworks_and_drivers.discord_bot.view.members_table_view import MembersQttView
from project.frameworks_and_drivers.discord_bot.view.embed_middleware import get_emb_without_author
from time import time

@MW_BOT.bot.command()
async def get_report_members(ctx: commands.Context, format: str, last_days: int = 7):

    time_start: float = time()

    possib_format: Tuple[str, str] = ("chart", "table")
    if format not in possib_format:
        await ctx.reply("❌ WRONG COMMAND: 'format' only accepts \'chart\' and \'table\'")
        return

    #First contact
    PREP_MSG: str = "🔄 grabbing and preparing the data . . ."
    await ctx.reply(PREP_MSG)

    #Getting and checking the server
    server: Guild = ctx.guild
    if server is None:
        await ctx.reply("Access not allowed due to discord permissions")
        return

    #Calling the data throughout the API
    URL: str = os.getenv("BASE_URL") + f"/member_analysis?server_id={server.id}"
    resp: Response = get(URL)
    
    #Sending a response when the request is unsuccessful
    if resp.status_code != 200:
        await ctx.reply(f"Something went bad in the backend --> Status: {resp.status_code}")
        return
    
    ds: Dict[str, Any] = resp.json()

    #Encapsulating the data in a beautiful interface and sending it as response
    view: MembersQttView = MembersQttView(
        members_in_dataset = ds["data"],
        num_of_days = last_days,
        overall_tot_avg = ds["overall_tot_avg"],
        overall_tot_std_dev = ds["overall_tot_std_dev"],
        overall_var_avg = ds["overall_var_avg"],
        overall_var_std_dev = ds["overall_var_std_dev"]
    )

    if format == "table": #<--- The user wants a table
        await ctx.reply(str(view))
    
    if format == "chart": #<--- The user wants a graph
        #Building the curve
        MembersGraph.build_curve(
            days = [data_day[0] for data_day in ds["data"].values()],
            qtts = [data_day[3] for data_day in ds["data"].values()],
            server_id = server.id
        ) #Saves the figure in a repository
        
        time_end: float = time()
        t_interval: float = time_end - time_start

        #Preparing the embeding
        emb, file = get_emb_without_author(
            title = "🔗 Graphical information about the quantity of members",
            desc = view.get_desc(into_embed = True),
            footer_txt = f"Backend latency: {t_interval:.4f} sec",
            img_path = f"{MembersGraph.REPO_PATH}/members_{server.id}.png"
        )
        
        #Replying with the image
        await ctx.reply(
            embed = emb,
            file = file
        )

        #Deleting the image from the repo
        os.remove(f"{MembersGraph.REPO_PATH}/members_{server.id}.png")

@get_report_members.error
async def error_get_report_members(ctx: commands.Context, ERR: Any):

    END_MSG: str = """\n
The command has the format: wolf?show_members_qtt format last_days. For example:\n
'wolf?show_members_qtt table 5' will show the quantity of members for the last 5 days in a table.\n
Instead of table, you can use a chart to see the data in a chart!"""

    if isinstance(ERR, commands.MissingRequiredArgument):
        await ctx.reply("❌ WRONG COMMAND: you forgot to define all parameters." + END_MSG)
    elif isinstance(ERR, commands.BadArgument):
        await ctx.reply("❌ WRONG COMMAND: the third parameter must be a number" + END_MSG)