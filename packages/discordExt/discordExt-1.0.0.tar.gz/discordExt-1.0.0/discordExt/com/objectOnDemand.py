
import asyncio
from dataclasses import dataclass
import typing

from discord import Guild
from discordExt.funcs.get import get, get_or_fetch
from discordExt.utils.store.driver import Driver
from discordExt.utils.store.driverGroup import DriverGroup
from discordExt.utils.store.memdriver import MemoryDriver
from discord.ext import commands

@dataclass
class DiscordObjectSpecifier:
    type : typing.Literal["CHANNEL", "USER", "ROLE", "EMOJI", "GUILD"]
    id : int
    depends_on : int = None

class DiscordObjectDriver(MemoryDriver):
    """
    this is a async ready driver with the purpose of getting discord objects on demand
    """
    settable : bool =False
    _internal_driver : Driver = None
    _quick_id_objects : dict = {}
    
    def __init__(self, driver : typing.Union[Driver, DriverGroup, dict], **data) -> None:
        super().__init__(**data)
        object.__setattr__(self, "_internal_driver", driver)
        # check driver
        for key, val in self._internal_driver.items():
            if key.startswith("_"):
                continue
        
            if not isinstance(val, (DiscordObjectSpecifier, dict)):
                raise TypeError(f"Expected DiscordObjectSpecifier or dict got {type(val)}")
        object.__setattr__(self._internal_driver,"settable", False)
        # 
        object.__setattr__(self, "_quick_id_objects", {})
        
    def get(self, key: str, depender : typing.Union[Guild, commands.Bot] = None, useFetch : bool = True):
        
        item : typing.Union[dict, DiscordObjectSpecifier] = self._internal_driver.get(key, None)
        if item is None:
            return None
        
        type_ = item.get("type") if isinstance(item, dict) else item.type
        id_ = item.get("id") if isinstance(item, dict) else item.id
        depends_on = item.get("depends_on") if isinstance(item, dict) else item.depends_on
        
        if id_ in self._quick_id_objects:
            return self._quick_id_objects[id_]
        
        if depends_on is not None and depends_on not in self._quick_id_objects:
            # attempt to get depends on object
            depends_on_obj = self.get(depends_on)
            if depends_on_obj is None:
                raise ValueError(f"Could not get depends on object {depends_on}")
            
            depender = self._quick_id_objects.get(depends_on)
        
        if useFetch:
            val = asyncio.run_coroutine_threadsafe(get_or_fetch(id_, depender, type_), asyncio.get_event_loop()).result()
        else:
            val= get(id_, depender, type_)

        if val is not None:
            self._quick_id_objects[id_] = val
    
    async def load_all(self, bot : commands.Bot):
        
        
        for key, val in self._internal_driver.items():
            depender = bot
            
            if key.startswith("_"):
                continue
                
            if not isinstance(val, (DiscordObjectSpecifier, dict)):
                raise TypeError(f"Expected DiscordObjectSpecifier or dict got {type(val)}")
            
            type_ = val.get("type") if isinstance(val, dict) else val.type
            id_ = val.get("id") if isinstance(val, dict) else val.id
            depends_on = val.get("depends_on") if isinstance(val, dict) else val.depends_on
            
            if id_ in self._quick_id_objects:
                continue
            
            if depends_on is not None and depends_on not in self._quick_id_objects:
                # attempt to get depends on object
                depends_on_obj = self.get(depends_on)
                if depends_on_obj is None:
                    raise ValueError(f"Could not get depends on object {depends_on}")
                
                depender = self._quick_id_objects.get(depends_on)
            
            val = await get_or_fetch(id_, depender, type_)
            if val is not None:
                self._quick_id_objects[id_] = val
                
            