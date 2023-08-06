
from discordExt.utils.store.driver import Driver

class MemoryDriver(Driver):
    gettable : bool = True
    settable : bool = True
    deletable : bool = True
    savable : bool = False
    