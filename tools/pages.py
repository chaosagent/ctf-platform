from functools import wraps

from flask import g, render_template
from flask_login import current_user

import config
import tools


def set_up_globals(current_page):
    g.ctf_name = config.platform.CTF_NAME
    g.show_problems_unauthed = config.platform.PROBLEMS_AVAILABLE_WITHOUT_LOGIN
    g.current_page = current_page
    g.authed = current_user.is_authenticated()
    g.competition_active = tools.general.competition_active()
    g.competition_started = tools.general.competition_started()
    g.competition_ended = tools.general.competition_ended()

# Wrapper to set up globals
def page(current_page):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            set_up_globals(current_page)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def gen_page_competition_inactive():
    return render_template('competition_inactive.html')

def competition_active_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if tools.general.competition_active() == -1:
            return gen_page_competition_inactive()
        else:
            return func(*args, **kwargs)
    return wrapper

def competition_started_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not tools.general.competition_started():
            return gen_page_competition_inactive()
        else:
            return func(*args, **kwargs)
    return wrapper