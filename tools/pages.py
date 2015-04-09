from functools import wraps

from flask import g

import config


def set_up_globals():
    g.ctf_name = config.platform.CTF_NAME

# Wrapper to set up globals
def page(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        set_up_globals()
        return func(*args, **kwargs)
    return wrapper