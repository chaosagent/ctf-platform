from flask import render_template, Blueprint, request

import api
import tools

app = Blueprint('page_login', __name__)

@app.route('/login', methods=['GET', 'POST'])
def page_login():
    if request.method == 'POST':
        result = api.accounts.login(**tools.general.unpack_request_data(**request.form))
        return render_template('login.html', success=result['success'], message=result['message'])
    return render_template('login.html')