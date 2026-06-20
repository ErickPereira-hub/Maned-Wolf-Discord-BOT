from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild
from typing import Dict, Any, Tuple, List
from requests import Response, get
from time import time
from project.frameworks_and_drivers.discord_bot.view.get_prob_new_members_view.get_single_prob_new_members_view import SingleProbNewMembersView
import os

@MW_BOT.bot.command()
async def get_prob_new_members(ctx: commands.Context, from_qtt: int, until_qtt: int, show: str = "no"):
    
    #Checking the parameters
    if from_qtt < 1 or until_qtt < from_qtt:
        await ctx.reply("❌ WRONG COMMAND: the first and second arguments must be positive numbers and the second can't be lower than the first")
        return
    
    #Checking if we can access the discord server
    server: Guild = ctx.guild
    if server is None:
        await ctx.reply("❌ Access not allowed due to discord permissions")
        return
    
    #First contact
    PREP_MSG: str = "🔄 grabbing the data and evaluating the probability . . ."
    await ctx.reply(PREP_MSG)
    
    #Calling the data throughout the API
    URL: str = os.getenv("BASE_URL") + f"/member_poisson?server_id={server.id}&from_qtt={from_qtt}&until={until_qtt}&show={show}"
    resp: Response = get(URL)
    status: int = resp.status_code

    #If we get into trouble with the API:
    if status != 200:
        
        if status == 403:
            await ctx.reply(f"⚠️ {resp.json()["message"]}")
            return

        await ctx.reply(f"❌ problem during a request to the API\nProblem Status ---> {status}\n\n {resp.json()["message"]}")
        return
    
    if show != "show":
        data: float = resp.json()["data"]
        await ctx.reply(str(SingleProbNewMembersView(prob = data, from_qtt = from_qtt, to_qtt = until_qtt)))
        return
    
    await ctx.reply(str(resp.json()))