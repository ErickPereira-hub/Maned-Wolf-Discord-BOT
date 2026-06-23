from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild, Member
from typing import Dict, Any
from requests import Response, get
from time import time
import os
from project.frameworks_and_drivers.discord_bot.view.predict_members_qtt_view import ViewPredictMembersQtt

@MW_BOT.bot.command()
async def predict_members_qtt(ctx: commands.Context,
                                    day: int = 1,
                                    show_poly: str = "no"):
    
    time_start: float = time() #<--- Begining

    if day > 3 or day < 1:
        await ctx.reply("❌ Range of days not allowed. You can do predictions from 1 to 3 days from now on")
        return

    server: Guild = ctx.guild #<--- Server where the request was done
    author: Member = ctx.author
    if server is None or author is None: #<--- Discord isn't allowing the access to the server
        BAD_MSG_DUE_TO_DISC: str = "❌ Access not allowed due to discord permissions!"
        await ctx.reply(BAD_MSG_DUE_TO_DISC)
        return

    #Sending an await message
    FIRST_MSG: str = "⚙️ Evaluating the results . . ."
    await ctx.reply(FIRST_MSG)

    #Requesting the data to the API
    URL: str = os.getenv("BASE_URL") + f"/member/predict?server_id={server.id}&day={day}&member_id={author.id}"
    resp: Response = get(URL)
    status: int = resp.status_code

    #If we get into trouble with the API:
    if status != 200:
        
        if status == 429:
            await ctx.reply(f"❌ Too many requests. Hold on, please!")
            return

        if status == 403:
            await ctx.reply("⚠️ You must have at least 10 days of data concerning the members before doing time predictions")
            return

        await ctx.reply(f"❌ problem during a request to the API\nProblem Status ---> {status}\n\n {resp.json()["message"]}")
        return
    
    #This piece of code will run if everything went fine (status as 200)
    data: Dict[str, Any] = resp.json()
    
    time_end: float = time() #<--- End of the process
    interval: float = time_end - time_start #<--- Interval of execution in seconds
    
    MSG: str = str(ViewPredictMembersQtt(
        day = day,
        show_poly = show_poly,
        resp = data,
        latency = interval
    ))
    await ctx.reply(MSG)

@predict_members_qtt.error
async def error_predict_members_qtt(ctx: commands.Context, ERR: Exception):

    END_MSG: str = """
        The command has the format wolf?predict_members_qtt day show_poly, where
        day is an integer that defines the day in the future (1 is tomorrow, 2 is one day after tomorrow etc.)
        and show_poly can be \'show\', which means that you want to see the best fit polynomial used to predict
        your result. You don't need to define these parameters because they have default values (day = 1 and show_poly = \"no\")
    """
    
    if isinstance(ERR, commands.BadArgument):
        await ctx.reply("❌ WRONG COMMAND: the first parameter must be a number" + END_MSG)