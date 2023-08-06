"""
this module consists of discord string parsing and manipulation functions 
"""

from enum import Enum as _enum

class STRING_TYPE(_enum):
    TEXT = 0
    
    CHANNEL = 1
    EMOJI = 2
    EMOJI_ID = 3
    USER = 4
    ROLE = 5
    
    DATE : 10
    DATE_REL = 11
    DATE_SHORT = 12



RICH_TYPE_BEGINNING_INDICATORS = ["<#", "<:", "<@&", "<@", "<t:"]
RICH_TYPE_ENDING_INDICATORS = [">", ":>", ":R>", ":t>"]
RICH_TYPE_INDICATORS = RICH_TYPE_BEGINNING_INDICATORS +RICH_TYPE_ENDING_INDICATORS
RICH_TYPE_RE = r"|".join(RICH_TYPE_INDICATORS)

def sus_rich_type(string : str):
    if not string:
        return False
    
    if not any(string.startswith(i) for i in RICH_TYPE_BEGINNING_INDICATORS):
        return False
    
    if not any(string.endswith(i) for i in RICH_TYPE_ENDING_INDICATORS):
        return False
    
    return True


def sus_compound(string : str) -> bool:
    """
    check if it is a compound text
    
    both RICH_TYPE_BEGINNING_INDICATORS and RICH_TYPE_ENDING_INDICATORS has at least one element in string
    
    """
    if not string:
        return False
    
    if not any(i in string for i in RICH_TYPE_BEGINNING_INDICATORS):
        return False
    
    if not any(i in string for i in RICH_TYPE_ENDING_INDICATORS):
        return False
    
    return True


def get_type(string : str):
    if "<" not in string and ">" not in string:
        return STRING_TYPE.TEXT, string 
    
    if (
        string.startswith("<#") 
        and string.endswith(">") 
        and len(string) > 3
    ):
        return STRING_TYPE.CHANNEL, string[2:-1]
    # check is emoji
    elif (
        string.startswith("<:") 
        and string.endswith(":>") 
        and len(string) > 5 
        and ":" in string[2:-2]
    ):
        return STRING_TYPE.EMOJI, string[2:-2]
    
    # check is role mention
    elif (
        string.startswith("<@&") 
        and string.endswith(">") 
        and len(string) > 4 
        and (val := string[3: -1]).isnumeric()
    ):
        return STRING_TYPE.ROLE, val
    # check is user mention
    elif (
        string.startswith("<@") 
        and string.endswith(">") 
        and len(string) > 4 
        and ((val := string[2: -1]).isnumeric() or (val := string[3: -1]).isnumeric())
    ):
        return STRING_TYPE.USER, val
    # check is date relative
    elif (
        string.startswith("<t:") 
        and string.endswith(":R>") 
        and len(string) > 6 
        and (val := string[3: -3]).isnumeric()
    ):
        return STRING_TYPE.DATE_REL, val
    elif (
        string.startswith("<t:") 
        and string.endswith(":t>") 
        and len(string) > 6 
        and (val := string[3: -3]).isnumeric()
    ):
        return STRING_TYPE.DATE_SHORT, val
    elif (
        string.startswith("<t:") 
        and string.endswith(">") 
        and len(string) > 4 
        and (val := string[3: -1]).isnumeric()
    ):
        return STRING_TYPE.DATE, val
    
    return STRING_TYPE.TEXT, string

class TEXT_FORMAT(_enum):
    BOLD =1
    ITALIC =2
    UNDERLINE =3
    STRIKETHROUGH =4
    CODEBLOCK =5
    CODEBLOCK_WITH_DECO =6
    CODE = 7
    SPOILER = 8

def get_styles(string : str):
    formats : list = []
    meta : dict = {}
    
    if not any([x for x in string if x in ["*","_","`","~","|"]]):
        return string
    
    while True:
        compare = string
        if string.startswith("**") and string.endswith("**"):
            formats.append(TEXT_FORMAT.BOLD)
            string = string[2:-2]
        elif string.startswith("*") and string.endswith("*"):
            formats.append(TEXT_FORMAT.ITALIC)
            string = string[1:-1]
        elif string.startswith("__") and string.endswith("__"):
            formats.append(TEXT_FORMAT.UNDERLINE)
            string = string[2:-2]
        elif string.startswith("~~") and string.endswith("~~"):
            formats.append(TEXT_FORMAT.STRIKETHROUGH)
            string = string[2:-2]
        elif string.startswith("```") and string.endswith("```"):
            string = string[3:-3]
            
            if "\n" in string and string.index("\n") < 10:
                split = string.split("\n", 1)
                meta["deco"] = split[0]
                string = split[1]
                formats.append(TEXT_FORMAT.CODEBLOCK_WITH_DECO)
            else:
                formats.append(TEXT_FORMAT.CODEBLOCK)
        elif string.startswith("`") and string.endswith("`"):
            formats.append(TEXT_FORMAT.CODE)
            string = string[1:-1]
        elif string.startswith("||") and string.endswith("||"):
            formats.append(TEXT_FORMAT.SPOILER)
            string = string[2:-2]

        if compare == string:
            break
    
    meta["format"] = formats
    meta["string"] = string
    
    return meta