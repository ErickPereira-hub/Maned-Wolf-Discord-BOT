import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from time import sleep
from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from project.domain.interfaces.bot_interfaces.bot import Bot

if __name__ == "__main__":
    sleep(20)
    bot: Bot = MW_BOT
    bot.start()