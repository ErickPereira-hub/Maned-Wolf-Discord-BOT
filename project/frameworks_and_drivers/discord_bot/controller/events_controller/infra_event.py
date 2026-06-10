from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT

@MW_BOT.bot.event
async def on_ready() -> None:
    print("Started")