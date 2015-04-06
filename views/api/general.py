from flask import Blueprint, request
from flask_login import login_required

import tools


app = Blueprint('api_general', __name__)

def api_test(args):
    return tools.api.gen_result_success(args)

@app.route('/api/test', methods=['GET', 'POST'])
@tools.api.response
def public_api_test():
    return api_test(request.args if request.method == 'GET' else request.form)

def api_test2(args):
    return tools.api.gen_result_success(args)

@app.route('/api/test2', methods=['GET', 'POST'])
@login_required
@tools.api.response
def public_api_test2():
    return api_test2(request.args if request.method == 'GET' else request.form)