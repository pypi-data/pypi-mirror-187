
import typing
from discordExt.utils.store.driver import Driver

_not_found =object()

class DriverGroup(list):
    MODES : typing.Literal["STD", "MIRROR", "COLLECTION"]
    
    class Config:
        pass
    
    def __init__(self, *args):
        super().__init__()
        self.MODE = "STD"
        self.CONFIG = self.Config()
        for arg in args:
            if not isinstance(arg, Driver):
                raise TypeError(f"Expected Driver got {type(arg)}")
            
            self.append(arg)
            
    # wrap all operations with checks to be Driver Type
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            index, key = key
            if not isinstance(index, int):
                raise TypeError(f"Expected int got {type(index)}")
            
            if not isinstance(key, str):
                raise TypeError(f"Expected str got {type(key)}")
            
            self[index][key] = value
        elif isinstance(key, int) and isinstance(value, Driver):
            super().__setitem__(key, value)
        elif isinstance(key, str):
            self._perform_set(key, value)
            
            
    def __iadd__(self, other):
        if not isinstance(other, Driver):
            raise TypeError(f"Expected Driver got {type(other)}")
        
        return super().__iadd__(other)
    
    def __add__(self, other):
        if not isinstance(other, Driver):
            raise TypeError(f"Expected Driver got {type(other)}")
        
        return super().__add__(other)
    
    def __radd__(self, other):
        if not isinstance(other, Driver):
            raise TypeError(f"Expected Driver got {type(other)}")
        
        return super().__radd__(other)
    
    def __imul__(self, other):
        if not isinstance(other, Driver):
            raise TypeError(f"Expected Driver got {type(other)}")
        
        return super().__imul__(other)
    
    def __mul__(self, other):
        if not isinstance(other, Driver):
            raise TypeError(f"Expected Driver got {type(other)}")
        
        return super().__mul__(other)
    
    def __rmul__(self, other):
        if not isinstance(other, Driver):
            raise TypeError(f"Expected Driver got {type(other)}")
        
        return super().__rmul__(other)
    
    def __contains__(self, item):
        if isinstance(item, Driver):    
            return super().__contains__(item)
        if (
            isinstance(item, tuple) 
            and len(item) == 2 
            and isinstance((index :=item[0]), int) 
            and isinstance((key := item[1]), str)
        ):
            return key in self[index]
        
        if isinstance(item, str):
            for driver in self:
                driver : Driver
                if item in driver:
                    return True
                
            return False
    
        raise TypeError(f"Expected Driver or (int, str) got {type(item)}")
    #
    
    def __getitem__(self, key : typing.Union[str, int]):
        if isinstance(key, int):
            return super().__getitem__(key)
        elif isinstance(key, str):
            return self._perform_get(key)
        
        raise TypeError(f"Expected int or str got {type(key)}")
                
    def reorder(self, *numbers : typing.List[int]):
        if len(numbers) != len(self):
            raise ValueError(f"Expected {len(self)} numbers got {len(numbers)}")
        
        copy = self.copy()
        self.clear()
        for i, num in enumerate(numbers):
            self.append(copy[num])
    
    # 
    def _perform_set(self, key : str, val):
        if self.MODE == "STD":
            for driver in self:
                driver : Driver
                if not driver.settable:
                    continue
                driver[key] = val
                break    
        elif self.MODE == "MIRROR":
            for driver in self:
                driver : Driver
                if not driver.settable:
                    continue
                driver[key] = val
        elif self.MODE == "COLLECTION":
            if not isinstance(val, (list, set, tuple)):
                raise TypeError(f"Expected list, set, or tuple got {type(val)}")
            
            if len(val) != len(self):
                raise ValueError(f"Expected {len(self)} values got {len(val)}")
            
            for driver, value in zip(self, val):
                driver : Driver
                if not driver.settable:
                    raise ValueError(f"Driver {driver} is not settable")
                driver[key] = value
            
    def _perform_get(self, key : str):
        if self.MODE == "COLLECTION":
            return [driver[key] for driver in self]
        else:
            for driver in self:
                driver : Driver
                if not driver.gettable:
                    continue
                return driver[key]
            
    #
    
    def get(self, key : str, default = _not_found):
        try:
            return self._perform_get(key)
        except:
            if default is _not_found:
                raise
            else:
                return default
            
    def set(self, key : str, val):
        self._perform_set(key, val)