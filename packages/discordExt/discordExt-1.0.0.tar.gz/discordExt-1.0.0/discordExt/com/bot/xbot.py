
from discord import Intents
from discordExt.com.bot.onDemand import xBotOndemandCache
from discordExt.com.objectOnDemand import DiscordObjectDriver
from discord.ext.commands import Bot

class xBot(Bot, xBotOndemandCache):
    async def setup_hook(self) -> None:
        await self.tree.sync()
        await super().setup_hook()

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.x_odc_load()
        
    @property
    def cache(self):
        return self.x_odc_cache
    
    @classmethod
    def default(
        command_prefix ="!",
        intents=Intents.all()
    ):
        return xBot(
            command_prefix=command_prefix,
            intents=intents
        )