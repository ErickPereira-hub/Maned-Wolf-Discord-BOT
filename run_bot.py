from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from project.domain.interfaces.bot_interfaces.bot import Bot

bot: Bot = MW_BOT
bot.start()