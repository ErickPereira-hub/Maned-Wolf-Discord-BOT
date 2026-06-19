from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from discord import Guild
from typing import Dict, Any, Tuple
from requests import Response, get
from time import time
import os
from project.frameworks_and_drivers.discord_bot.view.predict_members_qtt_between_view import ViewPredictMembersQttBetween

@MW_BOT.bot.command()
async def predict_members_qtt_between(ctx: commands.Context,
                                    day: int = 7,
                                    show_poly: str = "no"):
    
    time_start: float = time()

    if day > 7:
        await ctx.reply("Range of days not allowed. You can do predictions for an interval inside the interval from 1 to 7")
        return

    #Sending an await message
    FIRST_MSG: str = "⚙️ Evaluating the results . . ."
    await ctx.reply(FIRST_MSG)

    server: Guild = ctx.guild
    if server is None:
        BAD_MSG_DUE_TO_DISC: str = "❌ Access not allowed due to discord permissions!"
        await ctx.reply(BAD_MSG_DUE_TO_DISC)
        return

    #Requesting the data to the API
    URL: str = os.getenv("BASE_URL") + f"/member_predict?server_id={server.id}&day={day}"
    resp: Response = get(URL)
    status: int = resp.status_code

    #If we get into trouble with the API:
    if status != 200:
        
        if status == 403:
            await ctx.reply("⚠️ You must have at least 10 days of data concerning the members before doing time predictions")
            return

        await ctx.reply(f"❌ problem during a request to the API\nProblem Status ---> {status}\n\n {resp.json()["message"]}")
        return
    
    #This piece of code will run if everything went fine (status as 200)
    data: Dict[str, Any] = resp.json()
    
    time_end: float = time()
    interval: float = time_end - time_start #<--- Interval of execution in seconds
    
    MSG: str = str(ViewPredictMembersQttBetween(
        day = day,
        show_poly = show_poly,
        resp = data,
        latency = interval
    ))
    await ctx.reply(MSG)