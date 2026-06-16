import discord
from discord.ext import commands
from project.domain.interfaces.bot_interfaces.bot import Bot
import os

class ManedWolfDiscordBot(Bot):

    def __init__(self,
                name: str = "Maned Wolf Data",
                description: str = "Maned Wolf Data is a bot that performs advanced data analysis on your server\'s datasets, delivering real-time insights through simple commands. Beyond that, it provides future predictions powered by statistical models and machine learning, helping you anticipate trends and make informed decisions.",
                prefix: str = "wolf?"):
        self.name: str = name
        self.description: str = description
        self.__prefix: str = prefix
        self.__intents: discord.Intents = discord.Intents.all()
        self.__bot: commands.Bot = commands.Bot(command_prefix=self.__prefix, intents = self.__intents)
    
    def start(self, TOKEN: str = os.getenv("BOT_TOKEN")) -> None:
        self.__bot.run(TOKEN)
    
    @property
    def bot(self) -> commands.Bot:
        return self.__bot