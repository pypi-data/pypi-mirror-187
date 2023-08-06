

from types import MappingProxyType
from discordExt.utils.store.driver import PathDriver
from discordExt.utils.json import JSON

class JsonDriver(PathDriver):
    gettable : bool = True
    settable : bool = True
    deletable : bool = True
    savable : bool = True 
    
    def load(self, path : str):
        return JSON.load_file(path)
        
    def save(self):
        super().save()
        JSON.save_file(self.path, self.data)

import toml

class TomlDriver(PathDriver):
    gettable : bool = True
    settable : bool = True
    deletable : bool = True
    savable : bool = True 
    
    def load(self, path : str):
        return toml.load(path)
        
    def save(self):
        super().save()
        with open(self.path, "w") as f:
            toml.dump(self.data, f)
    
class PyDriver(PathDriver):
    gettable : bool = True
    settable : bool = False
    deletable : bool = False
    savable : bool = False

    def load(self, path : str):
        data = {}
        with open(path, "r") as f:
            exec(f.read(), data)
        return MappingProxyType(data)
    