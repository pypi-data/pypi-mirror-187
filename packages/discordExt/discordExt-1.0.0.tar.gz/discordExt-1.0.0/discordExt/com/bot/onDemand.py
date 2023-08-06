import typing
from discord.ext.commands import Bot
from discordExt.com.objectOnDemand import DiscordObjectDriver
from discordExt.utils.store.driver import Driver
from discordExt.utils.store.memdriver import MemoryDriver

class xBotOndemandCache:
    x_odc_cache : DiscordObjectDriver = None
    x_odc_config_load_on_ready : bool = True
    
    def x_odc_add_cache(self, driver : typing.Union[Driver, MemoryDriver, DiscordObjectDriver]):
        if isinstance(driver, DiscordObjectDriver):
            self.x_odc_cache = driver
        elif isinstance(driver, Driver):
            self.x_odc_cache = DiscordObjectDriver(driver)
        else:
            raise TypeError("driver must be a Driver or DiscordObjectDriver")
        
    async def x_odc_load(self, force : bool = False):
        if not self.x_odc_config_load_on_ready and not force:
            return 
        
        if not isinstance(self, Bot):
            raise TypeError("self is not a Bot")
        
        if not self.x_odc_cache:
            return
        
        await self.x_odc_cache.load_all(self)
        