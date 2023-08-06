import typing
from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass
from typing import Any

from discordExt.utils.json import JSON

class DriverMeta(ModelMetaclass):
    _singleton_instances = {}
    _non_singleton_paths = set()
    
    def __call__(cls, **kwds: Any) -> Any:
        singleton =kwds.get("singleton", True)
        path = kwds.get("path", None)
        
        if path is None:
            return super().__call__(**kwds)
        
        if path in cls._singleton_instances and not singleton:
            raise ValueError(f"Driver with path {path} is already a singleton")
        
        if path in cls._singleton_instances:
            return cls._singleton_instances[path]
        
        if singleton and path not in cls._non_singleton_paths:
            cls._singleton_instances[path] = super().__call__(**kwds)
            return cls._singleton_instances[path]
        elif singleton and path in cls._non_singleton_paths:
            raise ValueError(f"Driver with path {path} is already a non singleton")
    
        elif path not in cls._non_singleton_paths:
            cls._non_singleton_paths.add(path)
            
        return super().__call__(**kwds)
             
            
class Driver(BaseModel, metaclass=DriverMeta):
    _data : dict
    singleton : bool = True
    gettable : bool = False
    settable : bool = False
    deletable : bool = False
    savable : bool = False
    onChangeSave : bool = True
    
    class Config:
        frozen = True
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._init_load()
        

    def _init_load(self):
        object.__setattr__(self, "_data", {})
        
    def get(self, key: str, default=None):
        if not self.gettable:
            raise ValueError("This driver is not gettable")
        return self.data.get(key, default)

    def set(self, key: str, value):
        if not self.settable:
            raise ValueError("This driver is not settable")
        if value == self.data.get(key, None):
            return
        
        self.data[key] = value
    
    def __getitem__(self, key: str):
        return self.get(key)
    
    def __setitem__(self, key: str, value):
        return self.set(key, value)
    
    def __contains__(self, key: str):
        return key in self.data
    
    def delete(self, key : str):    
        if not self.deletable:
            raise ValueError("This driver is not deletable")
        del self.data[key]
        
    
    def __delitem__(self, key : str):
        return self.delete(key)
        
    def items(self):
        return self.data.items()
    
    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def __iter__(self):
        return iter(self.data)
    
    def len(self):
        return len(self.data)
    
    @property
    def data(self):
        return self._data
    
class PathDriver(Driver):
    path : str
    _complex_hash : dict

    def set(self, key: str, value):
        super().set(key, value)
        if not self.savable:
            return
        if self.onChangeSave:
            self.save()
    
    def get(self, key: str, default=None):
        val = super().get(key, default)
        if not self.savable:
            return val
        
        if self.onChangeSave and (new_hash := hash(JSON.dumps_json(val))) != self._complex_hash.get(key, None):
            self.save()
            self._complex_hash[key] = new_hash
        return val
        
    def __init__(self, **data) -> None:
        super().__init__(**data)
        object.__setattr__(self, "_complex_hash", {})
    
    def load(self, path : str):
        raise NotImplementedError()

    def save(self):
        if not self.savable:
            raise ValueError("This driver is not savable")
    
    def _init_load(self):
        object.__setattr__(self, "_data", self.load(self.path))
        
        
    def delete(self, key: str):
        super().delete(key)
        if not self.savable:
            return
        if self.onChangeSave:
            self.save()