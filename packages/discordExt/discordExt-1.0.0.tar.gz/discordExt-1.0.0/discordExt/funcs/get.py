import typing
import discord as _discord
from discord.ext import commands as _commands
from discord.abc import Messageable
async def _get_or_fetch(val : int, get_method : typing.Callable, fetch_method : typing.Callable):
    val = int(val)
    
    if get_method is not None:
        val = get_method(val)
    else:
        val = None
    if val is None:
        return await fetch_method(val)
    
    return val

def _resolve_target_str(target : str):
    if target == "CHANNEL":
        target= Messageable
    elif target == "USER":
        target = _discord.User
    elif target == "ROLE":
        target = _discord.Role
    elif target == "EMOJI":
        target = _discord.Emoji
    elif target == "GUILD":
        target = _discord.Guild
    else:
        raise ValueError(f"Unknown target {target}")
    
    return target

async def get_or_fetch(val : int, depender : typing.Union[_commands.Bot, _discord.Guild], target : typing.Union[type, str]):
    if target is None:
        raise TypeError("target cannot be None")
    
    if not isinstance(target, (type,str)):
        raise TypeError(f"Expected type or str got {type(target)}")
    
    if isinstance(target, str):
        target = _resolve_target_str(target)
    
    if depender is None:
        raise TypeError("depender cannot be None")
    
    if target == _discord.User and isinstance(depender, _commands.Bot):
        return await _get_or_fetch(
            val,
            depender.get_user,
            depender.fetch_user
        )
    elif target == _discord.Guild and isinstance(depender, _commands.Bot):
        return await _get_or_fetch(
            val,
            depender.get_guild,
            depender.fetch_guild,
        )
    elif target == _discord.TextChannel and isinstance(depender, _discord.Guild):
        return await _get_or_fetch(
            val,
            depender.get_channel,
            depender.fetch_channel,
        )
    
    elif target == _discord.Role and isinstance(depender, _discord.Guild):
        return depender.get_role(val)
    
    elif target in [_discord.Member, _discord.User]  and isinstance(depender, _discord.Guild):
        return await _get_or_fetch(
            val,
            depender.get_member,
            depender.fetch_member,
        )
    # channel
    elif (target == Messageable or issubclass(target, Messageable)) and isinstance(depender, (_discord.Guild, _commands.Bot)):
        return await _get_or_fetch(
            val,
            depender.get_channel,
            depender.fetch_channel,
        )
    elif target == _discord.DMChannel and isinstance(depender, _discord.User):
        depender : _discord.user
        return await _get_or_fetch(
            
            val,
            depender.get_channel,
            depender.fetch_channel,
        )
    # message
    elif target == _discord.Message and isinstance(depender, Messageable):
        return await _get_or_fetch(
            val,
            None,
            depender.fetch_message,
        )
    elif target == _discord.Emoji and isinstance(depender, _discord.Guild):
        return await _get_or_fetch(
            val,
            None,
            depender.fetch_emoji,
        )
    else:
        raise TypeError("depender is not a valid type")
    
def get(val : int, depender : typing.Union[_commands.Bot, _discord.Guild], target : typing.Union[type, str]):
    if target is None:
        raise TypeError("target cannot be None")
    
    if not isinstance(target, (type,str)):
        raise TypeError(f"Expected type or str got {type(target)}")
    
    if isinstance(target, str):
        target = _resolve_target_str(target)
    
    if depender is None:
        raise TypeError("depender cannot be None")
    
    if target == _discord.User and isinstance(depender, _commands.Bot):
        return depender.get_user(val)
    elif target == _discord.Guild and isinstance(depender, _commands.Bot):
        return depender.get_guild(val)
    elif target == _discord.TextChannel and isinstance(depender, _discord.Guild):
        return depender.get_channel(val)
    
    elif target == _discord.Role and isinstance(depender, _discord.Guild):
        return depender.get_role(val)
    
    elif target in [_discord.Member, _discord.User]  and isinstance(depender, _discord.Guild):
        return depender.get_member(val)
    
    elif (target == Messageable or issubclass(target, Messageable)) and isinstance(depender, _discord.Guild):
        return depender.get_channel(val)
    elif target == _discord.DMChannel and isinstance(depender, _discord.User):
        depender : _discord.user
        return depender.get_channel(val)
    
    elif target == _discord.Message and isinstance(depender, Messageable):
        return depender.fetch_message(val)
    
    elif target == _discord.Emoji and isinstance(depender, _discord.Guild):
        return depender.fetch_emoji(val)
    
    else:
        raise TypeError("depender is not a valid type")