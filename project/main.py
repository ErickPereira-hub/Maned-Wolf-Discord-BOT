from frameworks_and_drivers.discord_bot.infra.singletons import NW_BOT
from frameworks_and_drivers.discord_bot.infra.named_wolf_bot import NamedWolfDiscordBot

if __name__ == "__main__":
    discord_bot: NamedWolfDiscordBot = NW_BOT
    discord_bot.start()