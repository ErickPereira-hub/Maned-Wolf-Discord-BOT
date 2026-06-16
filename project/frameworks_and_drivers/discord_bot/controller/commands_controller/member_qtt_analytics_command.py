from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild
from typing import Dict, Any, Tuple
import os
from requests import Response, get
from project.frameworks_and_drivers.discord_bot.view.members_table_view import MembersTable

@MW_BOT.bot.command()
async def show_members_qtt(ctx: commands.Context, format: str, last_days: int):

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
    
    #Encapsulating the data in a beautiful interface and sending it as response
    view: MembersTable = MembersTable(
        members_in_dataset = resp.json()["data"],
        num_of_days = last_days
    )
    
    await ctx.reply(str(view))

@show_members_qtt.error
async def error_show_members_qtt(ctx: commands.Context, ERR: Any):

    END_MSG: str = """\n
The command has the format: wolf?show_members_qtt format last_days. For example:\n
'wolf?show_members_qtt table 5' will show the quantity of members for the last 5 days in a table.\n
Instead of table, you can use a chart to see the data in a chart!"""

    if isinstance(ERR, commands.MissingRequiredArgument):
        await ctx.reply("❌ WRONG COMMAND: you forgot to define all parameters." + END_MSG)
    elif isinstance(ERR, commands.BadArgument):
        await ctx.reply("❌ WRONG COMMAND: the third parameter must be an number" + END_MSG)