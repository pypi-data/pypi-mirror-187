import contextlib
import cProfile
import pstats
import io
import typing

@contextlib.contextmanager
def profiler(self, print_stats=False):
    """
    a context manager for profiling
    
    ex:
    with self.profiler():
        # do something

    """
    
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    
    sortby = 'cumulative'
    s = io.StringIO()
    stats = pstats.Stats(pr, stream=s).sort_stats(sortby)
    stats.print_stats()
    
    if print_stats:
        print(s.getvalue())
        
def tryDelete(path : str):
    import os
    try:
        os.remove(path)
    except:
        pass
    
def quickDebug(
    lv :typing.Literal["info", "debug"] = "info",
    stream=None,
    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
):
    import logging
    import sys
    if stream is None:
        stream = sys.stdout
    
    logging.basicConfig(
        stream=stream,
        level=logging.DEBUG if lv == "debug" else logging.INFO,
        format=format
    )
    