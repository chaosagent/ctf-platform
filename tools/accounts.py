from flask import request, url_for
from flask_login import login_required
from werkzeug.utils import redirect

import tools


def public_not_logged_in():
    if request.path.split('/')[1] == 'api':
        return tools.api.api_response(tools.api.gen_result_unauthorized())
    else:
        return redirect(url_for('page_login.page_login'))

def login_required_if(conditional):
    if conditional:
        return login_required
    else:
        return lambda func: func