

from datetime import datetime
from functools import cached_property
import discord
from pydantic import BaseModel, Field, validator
import typing

from discordExt.funcs.parse import formatVars, parseVars
from typing import get_args

class BaseEmbedModel(BaseModel):
    
    
    class Config:
        keep_untouched = (cached_property,)
        
    @cached_property
    def _one_time_parse_format_vars(self):
        vals = {}
        unique = set()
        children = []
        
        for k, v in self.__fields__.items():
            # ignore complex case
            if len(get_args(v.type_)) > 0:
                continue
            
            #
            if v.type_ != str  and not issubclass(v.type_, BaseEmbedModel):
                continue
            
            if issubclass(v.type_, BaseEmbedModel) and getattr(self, k, None) is not None:
                children.append(k)
                continue

            
            rv = getattr(self, k, None)
            if rv is None:
                continue
            
            vals[k] = formatVars(rv)
            # add list to unique
            unique.update(vals[k])
        
        return vals, unique, children
    
    @property
    def _key_var_dict(self):
        return self._one_time_parse_format_vars[0]

    @property
    def _child_vars(self):
        return self._one_time_parse_format_vars[2]
    
    @property
    def _all_format_vars(self):
        return self._one_time_parse_format_vars[1]
    
    def _prepKwargs(self, defaults : dict, raise_insufficient_vars : bool = False,**kwargs):
        vars = {
            k: kwargs.get(k, defaults.get(k, None)) for k in self._all_format_vars
        }
        if raise_insufficient_vars and any(v is None for v in vars.values()):
            raise ValueError("insufficient vars")
        
        return vars
    
    def _formatField(self, key : str, raise_insufficient_vars : bool = False, **kwargs):
        kwargs = self._prepKwargs(raise_insufficient_vars,**kwargs)
        
        # format child
        if key in self._child_vars and (node := getattr(key, self, None)) is not None:
            node : BaseEmbedModel
            return node.format(**kwargs)
        
        if key in self._child_vars and node is None:
            return None
        
        # does not exist
        if key not in self._key_var_dict:
            return None
        
        # format key
        vars = self._key_var_dict.get(key)
        vars_prep = {k: kwargs.get(k, None) for k in vars}
        fstring : str = getattr(self, key)
        return fstring.format(**vars_prep)
                
    def format(self, defaults : dict=None,  raise_insufficient_vars : bool = False,**kwargs)-> 'EmbedModel':
        """
        format all fields and creates a EmbedModel
        """
        if defaults is None and hasattr(self, "_defaults"):
            defaults = getattr(self, "_defaults")
        
        okwargs = self._prepKwargs(defaults, raise_insufficient_vars,**kwargs)
        
        data = {}
        
        for var in self._key_var_dict:
            fstring : str = getattr(self, var)
            if fstring is None:
                continue
            
            sstring = fstring.format(**okwargs)
            data[var] = sstring
        
        for child in self._child_vars:
            node : BaseEmbedModel = getattr(self, child, None)
            
            if node is None:
                continue
            
            if isinstance(node, list):
                data[child] = [n.format(defaults, **kwargs) for n in node]  
            else:  
                data[child] = node.format(defaults, **kwargs)
        
        return self.__class__(**data)
                
class FooterModel(BaseEmbedModel):
    text : str
    icon_url : str = None

class AuthorModel(BaseEmbedModel):
    """
    embed author
    """
    name : str = None
    url : str = None
    icon_url : str = None

class EmbedFieldModel(BaseEmbedModel):
    """
    embed field
    """
    name : str
    value : str
    inline : bool = False

class EmbedModel(BaseEmbedModel):
    title : str = None
    description : str = None
    url : str = None
    color : int = None
    timestamp : datetime = None
    footer : FooterModel = None
    image : str = None
    thumbnail : str = None
    author : AuthorModel = None
    fields : typing.List[EmbedFieldModel] = None
    _defaults : dict
    
    @validator("timestamp",pre=True)
    def __to_datetime(val):
        if isinstance(val, (float,int)):
            return datetime.fromtimestamp(val)
        elif isinstance(val, str):
            return datetime.fromtimestamp(int(val))

        return val
    
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        object.__setattr__(self, "_defaults", {})
        
    @classmethod
    def fromEmbed(cls, embed : discord.Embed):
        title = embed.title
        description = embed.description
        url = embed.url
        color = embed._colour
        timestamp = embed.timestamp 
        image = embed.image.url if embed.image else None
        thumbnail = embed.thumbnail.url if embed.thumbnail else None
        fields = embed._fields
        
        
        footer = FooterModel(
            text=embed.footer.text, icon_url=embed.footer.icon_url
            ) if (
                embed.footer is not None and embed.footer.text is not None
            ) else None
        author = AuthorModel(name=embed.author.name, url=embed.author.url, icon_url=embed.author.icon_url) if embed.author is not None else None
        fields = [EmbedFieldModel(name=f.name, value=f.value, inline=f.inline) for f in embed.fields]
        
        return cls(
            title=title, 
            description=description, 
            url=url, color=color, 
            timestamp=timestamp, 
            footer=footer, 
            image=image, 
            thumbnail=thumbnail, 
            author=author, 
            fields=fields
        )
        
    def toEmbed(self):
        embed = discord.Embed(
            title=self.title, 
            description=self.description, 
            url=self.url, 
            color=self.color, 
            timestamp=self.timestamp
        )
        
        if self.footer is not None:
            embed.set_footer(text=self.footer.text, icon_url=self.footer.icon_url)
        
        if self.image is not None:
            embed.set_image(url=self.image)
        
        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)
        
        if self.author is not None:
            embed.set_author(name=self.author.name, url=self.author.url, icon_url=self.author.icon_url)
        
        if self.fields is not None:
            for f in self.fields:
                embed.add_field(name=f.name, value=f.value, inline=f.inline)
        
        return embed
    
    def _parse(self, fstring :str, sstring :str, fields : list, known : dict):
        for k, v in known.items():
            fstring = fstring.replace("{" + k + "}", str(v))
            
        res = parseVars(fstring, sstring, None, None)
        if res is None:
            raise ValueError("could not parse")
        
        known.update(res)
    
    def _parse_item(self, template_node, source_node, known):
        for key, var in template_node._key_var_dict.items():
            fstring : str = getattr(template_node, key)
            sstring : str = getattr(source_node, key)
            if fstring is None:
                continue
            
            self._parse(fstring, sstring, var, known)
    

    def parse(self, embed: discord.Embed):
        known = {}
        embedModel = self.fromEmbed(embed)

        for key, var in self._key_var_dict.items():
            fstring : str = getattr(self, key)
            sstring : str = getattr(embedModel, key)
            if fstring is None:
                continue
            
            self._parse(fstring, sstring, var, known)

        
        for child in self._child_vars:
            template_node : BaseEmbedModel = getattr(self, child, None)
            source_node : BaseEmbedModel = getattr(embedModel, child, None)
            
            if template_node is None or source_node is None:
                continue
            
            if isinstance(template_node, list):
                for t, s in zip(template_node, source_node):
                    self._parse_item(t, s, known)
                    
            else:
                self._parse_item(template_node, source_node, known)
            
                
        return known, embedModel
    
    