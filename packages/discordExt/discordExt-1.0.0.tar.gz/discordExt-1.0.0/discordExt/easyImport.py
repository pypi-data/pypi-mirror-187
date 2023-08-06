"""
provides easy import at the cost of performance

! ~~only intended for lazy people like me who just wanna to skip a few lines of code.~~ 
? ideal for quick deployment
"""

from discord.ext import commands
import discord
from discord import (
    Interaction, Embed, Guild, TextChannel, ForumChannel, GroupChannel, ForumTag, 
    Role, Member, User, Emoji, PartialEmoji, Message, MessageReference, File, 
    Asset, Invite, StageInstance, 
    StageChannel, Thread, ThreadMember,
    VoiceChannel, CategoryChannel, DMChannel, Colour, Color, 
    Permissions, PermissionOverwrite, Activity, ActivityType, Intents
)
from discord.ui import (
    View, Button, Select, Modal
)

from discord.ext.commands import (
    Bot, Cog, Context, Command, Group, CommandError, CommandNotFound, 
    CommandOnCooldown, MissingRequiredArgument, BadArgument, CheckFailure, CommandInvokeError, 
    MissingPermissions, NoPrivateMessage, NotOwner, 
    DisabledCommand, MissingRole, BotMissingPermissions, BotMissingRole
)
    