
from discord import Embed

class EmbedStatusWrapper:
    """
    helps to create quick embeds with status
    """
    
    def __init__(self, embed : Embed) -> None:
        self.embed = embed
    
    def success(self):
        self.embed.color = 0x00ff00
        return self.embed
    
    def error(self):
        self.embed.color = 0xff0000
        return self.embed
    
    def warning(self):
        self.embed.color = 0xffff00
        return self.embed
    
    def info(self):
        self.embed.color = 0x0000ff
        return self
    
class EmbedStatusAble:
    def success(self):
        self.color = 0x00ff00
        return self
    
    def error(self):
        self.color = 0xff0000
        return self
    
    def warning(self):
        self.color = 0xffff00
        return self
    
    def info(self):
        self.color = 0x0000ff
        return self