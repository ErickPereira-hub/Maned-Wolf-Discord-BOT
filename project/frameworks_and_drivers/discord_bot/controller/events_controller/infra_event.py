from frameworks_and_drivers.discord_bot.infra.singletons import NW_BOT

@NW_BOT.bot.event
async def on_ready() -> None:
    print("Started")