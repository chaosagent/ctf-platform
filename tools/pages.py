from functools import wraps

from flask import g
from flask_login import current_user

import config


def set_up_globals(current_page):
    g.ctf_name = config.platform.CTF_NAME
    g.show_problems_unauthed = config.platform.PROBLEMS_AVAILABLE_WITHOUT_LOGIN
    g.current_page = current_page
    g.authed = current_user.is_authenticated()

# Wrapper to set up globals
def page(current_page):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            set_up_globals(current_page)
            return func(*args, **kwargs)
        return wrapper
    return decorator