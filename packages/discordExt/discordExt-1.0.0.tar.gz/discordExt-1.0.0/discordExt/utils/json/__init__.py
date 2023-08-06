"""
this module provides smart loading for json parsing modules
"""

from typing import overload
import typing

class _Template:
    @overload
    def load_file(name : str): pass
    
    @overload
    def save_file(name : str, data: dict): pass

    @overload
    def loads_json(data): pass
    
    @overload
    def dumps_json(data): pass




"""
all methods are specified in the `_Template` class
by default, loaded modules will not be checked for methods
"""
JSON: _Template = None

def load_file(name : str):
    return JSON.load_file(name)

def save_file(name : str, data: dict): 
    return JSON.save_file(name , data)

def loads_json(data):
    return JSON.loads_json(data)

def dumps_json(data):
    return JSON.dumps_json(data)

def load_json(custom: typing.Union[str, object] = None, defaults = ["orjson","ujson","json"]):
    """
    smart loading of a json parsing module with preset methods
    
    by default, it will attempt to load module names present in defaults one by one in current module tree. If all fails, it will raise
    ```py
    load_json()
    ```
    
    if a custom str is passed in and part of the defaults, it will attempt to load the local module by that name
    if it is not part of the defaults, it will load the package using the standard `importlib.import_module`
    ```py
    load_json(custom="name")
    ```

    if custom is an object, it will check against the available methods (`validate`) and set JSON to the object
    ```py
    load_json(custom=wrapperObj)
    ```
    """
    
    global JSON
    
    # get current module
    import importlib, sys
    
    if custom is not None and not isinstance(custom, str):
        JSON = custom
        if not validate():
            JSON = None
            raise ImportError("custom json module does not have required methods")
        
    current_module = sys.modules[__name__]
    
    # get current module parent
    current_module_parent = current_module.__package__
    
    if custom is not None and (defaults is not None and custom in defaults):
        JSON = importlib.import_module(current_module_parent+"."+custom)
        return 
    elif custom is not None:
        JSON = importlib.import_module(custom)
        return
    
    for d in defaults:    
        try:
            JSON = importlib.import_module(current_module_parent+"."+d)
            return
        except ImportError as e:
            pass

    raise e
     
def validate()-> bool:
    global JSON, _Template
    
    if JSON is None:
        return False
    
    temp_methods = [x for x in dir(_Template) if not x.startswith("_")]
    for method in temp_methods:
        if not hasattr(JSON, method):
            return False
    
    return True


load_json() # attempt by default