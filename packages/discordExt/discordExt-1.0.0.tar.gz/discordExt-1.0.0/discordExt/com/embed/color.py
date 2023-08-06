
class EmbedColorable:
    def red(self):
        self.color = 0xff0000
        return self
    def green(self):
        self.color = 0x00ff00
        return self
    
    def blue(self):
        self.color = 0x0000ff
        return self
    
    def yellow(self):
        self.color = 0xffff00
        return self
    
    def cyan(self):
        self.color = 0x00ffff
        return self
    
    def magenta(self):
        self.color = 0xff00ff
        return self
    
    def black(self):
        self.color = 0x000000
        return self
    
from discord import Embed
    
class EmbedColorWrapper:
    def __init__(self, embed : Embed) -> None:
        self.embed = embed
        
    def red(self):
        self.embed.color = 0xff0000
        return self.embed
    
    def green(self):
        self.embed.color = 0x00ff00
        return self.embed
    
    def blue(self):
        self.embed.color = 0x0000ff
        return self.embed
    
    def yellow(self):
        self.embed.color = 0xffff00
        return self.embed
    
    def cyan(self):
        self.embed.color = 0x00ffff
        return self.embed
    
    def magenta(self):
        self.embed.color = 0xff00ff
        return self.embed
    
    def black(self):
        self.embed.color = 0x000000
        return self.embed