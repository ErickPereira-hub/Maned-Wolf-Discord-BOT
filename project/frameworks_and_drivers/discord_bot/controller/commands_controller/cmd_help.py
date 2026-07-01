from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord.ext import commands
from typing import List

@MW_BOT.bot.command()
async def cmd_help(ctx: commands.Context):

    #Reading the text inside the file with the documentation of the commands
    lines: List[str] | None = None
    with open("project/frameworks_and_drivers/discord_bot/src_static/commands.txt", "r") as FILE:
        lines = FILE.readlines()

    #Splitting the information in half because discord doesn't support huge messages
    num_lines: int = len(lines) // 2
    first_half_msg: str = "".join(lines[:num_lines])
    last_half_msg: str = "".join(lines[num_lines:])

    #Sending the text to the channel
    await ctx.reply(first_half_msg)
    await ctx.reply(last_half_msg)