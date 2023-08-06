import typing
from discordExt.funcs.str import *
from pydantic import BaseModel
from datetime import datetime
import discord
from discord.abc import Messageable
from discordExt.funcs.get import get, get_or_fetch
import re

class DcObjStr(BaseModel):
    """
    is a discord rich object representation in text format
    """
    
    type_ : STRING_TYPE
    text : typing.Union[str, int]
    _raw : str = None
    _changed : bool  = False
    
    def __init__(self, _raw : str = None, **data) -> None:
        super().__init__(**data)
        object.__setattr__(self, "_raw", _raw)
        object.__setattr__(self, "_changed", False)
        
    @property
    def uid(self):
        return int(self.text)
    
    @uid.setter
    def uid_setter(self, val):
        if not isinstance(val, (str, int)):
            raise TypeError("uid must be int or str")

        if val == self.uid or val == self.text:
            return
        
        self.text = val
        self._changed = True

    @classmethod
    def fromString(cls, string : str):
        typ, parsed = get_type(string)
        if typ == STRING_TYPE.TEXT:
            return None

        return cls(type_=typ, text=parsed, _raw = string)
    
    def toObj(self, depender):
        if self.type_ in [STRING_TYPE.DATE_REL, STRING_TYPE.DATE, STRING_TYPE.DATE_SHORT]:
            return datetime.fromtimestamp(int(self.text))
    
        if self.type_ == STRING_TYPE.CHANNEL:
            target_type = Messageable
        elif self.type_ == STRING_TYPE.USER:
            target_type = discord.User
        elif self.type_ == STRING_TYPE.ROLE:
            target_type = discord.Role
        elif self.type_ == STRING_TYPE.EMOJI:
            return get(self.text.split(":",1)[1], depender, discord.Emoji)
        else:
            raise ValueError("Cannot convert to object")
    
        return get(self.text, depender, target_type)

    async def asyncToObj(self, depender):
        if self.type_ in [STRING_TYPE.DATE_REL, STRING_TYPE.DATE, STRING_TYPE.DATE_SHORT]:
            return datetime.fromtimestamp(int(self.text))
    
        if self.type_ == STRING_TYPE.CHANNEL:
            target_type = Messageable
        elif self.type_ == STRING_TYPE.USER:
            target_type = discord.User
        elif self.type_ == STRING_TYPE.ROLE:
            target_type = discord.Role
        elif self.type_ == STRING_TYPE.EMOJI:
            return await get_or_fetch(int(self.text.split(":",1)[1]), depender, discord.Emoji)
        else:
            raise ValueError("Cannot convert to object")
    
        return await get_or_fetch(self.uid, depender, target_type)
        
    @property
    def mention(self):
        if not self._changed and self._raw is not None:
            return self._raw
        
        if self.type_ == STRING_TYPE.CHANNEL:
            return f"<#{self.text}>"
        elif self.type_ == STRING_TYPE.USER:
            return f"<@{self.text}>"
        elif self.type_ == STRING_TYPE.ROLE:
            return f"<@&{self.text}>"
        elif self.type_ == STRING_TYPE.EMOJI:
            return f"<:{self.text}>"
        elif self.type_ == STRING_TYPE.DATE:
            return f"<t:{self.text}>"
        elif self.type_ == STRING_TYPE.DATE_SHORT:
            return f"<t:{self.text}:t>"
        elif self.type_ == STRING_TYPE.DATE_REL:
            return f"<t:{self.text}:R>"
        else:
            raise ValueError("Cannot convert to mention")
        
class DcStr(BaseModel):
    text : str
    formats : typing.List[TEXT_FORMAT] = None
    _raw : str = None
    _changed : bool  = False
    _meta : dict = None
    
    def __init__(self, _raw : str = None, _meta : dict = None,**data):
        super().__init__(**data)
        object.__setattr__(self, "_raw", _raw)
        object.__setattr__(self, "_changed", False)
        object.__setattr__(self, "_meta", _meta)
    @classmethod
    def fromString(cls, string : str):
        meta_or_str = get_styles(string)
        if isinstance(meta_or_str, str):
            return cls(text=meta_or_str, _raw=string)

        meta = meta_or_str
        formats : list = meta.get("format")
        parsed_string = meta.get("string")

        return cls(text=parsed_string, _raw=string, formats=formats, _meta=meta)    

    def __str__(self):
        if not self._changed and self._raw is not None:
            return self._raw
        
        if self.formats is None:
            return self.text

        build_str = self.text
        for format in self.formats:
            if format == TEXT_FORMAT.BOLD:
                build_str = f"**{build_str}**"
            elif format == TEXT_FORMAT.ITALIC:
                build_str = f"*{build_str}*"
            elif format == TEXT_FORMAT.UNDERLINE:
                build_str = f"__{build_str}__"
            elif format == TEXT_FORMAT.STRIKETHROUGH:
                build_str = f"~~{build_str}~~"
            elif format == TEXT_FORMAT.CODE:
                build_str = f"`{build_str}`"
            elif format == TEXT_FORMAT.CODEBLOCK:
                build_str = f"```{build_str}```"
            elif format == TEXT_FORMAT.CODEBLOCK:
                build_str = f"```{self._meta.get('deco')}\n{build_str}```"
            elif format == TEXT_FORMAT.SPOILER:
                build_str = f"||{build_str}||"
            else:
                raise ValueError("Unknown format")

class DcText(BaseModel):
    texts : typing.List[typing.Union[DcStr, DcObjStr]]

    @classmethod
    def fromString(cls, string : str, focus_only : typing.List[STRING_TYPE] = None):
        # split by RICH_TYPE_BEGINNING_INDICATORS and RICH_TYPE_ENDING_INDICATORS
        
        splitted = re.split(f"({RICH_TYPE_RE})", string)
        splitted = [x for x in splitted if x != ""]
        
        raw = []
        op = False
        current = ""
        for split in splitted:
            if not op and split in RICH_TYPE_BEGINNING_INDICATORS:
                current += split
                op = True
            elif op and split in RICH_TYPE_ENDING_INDICATORS:
                raw.append(current+split)
                current = ""
                op = False
            elif split == ">" and not op:
                raw[-1] += ">"
            elif not op:
                raw.append(split)
            else:
                current += split
        
        for i in range(len(raw)):
            rich =sus_rich_type(raw[i])
            if rich:
                raw[i] = DcObjStr.fromString(raw[i])
            else:
                raw[i] = DcStr.fromString(raw[i])
        
        return cls(texts=raw)
        

def parseString(
    string : str,
):
    compound = sus_compound(string)
    rich =sus_rich_type(string)

    if compound:
        return DcText.fromString(string)
    elif rich:
        return DcObjStr.fromString(string)
    else:
        return DcStr.fromString(string)