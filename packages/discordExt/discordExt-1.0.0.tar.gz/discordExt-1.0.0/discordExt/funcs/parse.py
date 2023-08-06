"""
this module provides format variable parsing
"""
from string import Formatter
import parse

def formatVars(string :str):
    
    return [fn for _, fn, _, _ in Formatter().parse(string) if fn is not None]
    
def formatFullVars(string : str):
    return [x for x in Formatter().parse(string)]

def _slowParseVars(fstring : str, sstring : str, defaults : dict):
    """
    we make the assumption that no {}{} stacking vars
    """
    #todo, currently Im not sure how to handle this
    
    fstringVars = formatFullVars(fstring)
    pass

def parseVars(fstring : str, sstring : str, defaults : dict, allow_slow : bool = False):
    res =  parse.parse(fstring, sstring)
    if res is not None:
        return res.named

