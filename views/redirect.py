from flask import Blueprint, request, url_for
from flask import redirect as redirect_user


app = Blueprint('redirect', __name__)

@app.route('/redirect', methods=['GET', 'POST'])
def redirect():
    if 'next' in request.args:
        return redirect_user(request.args['next'])
    else:
        return redirect_user(url_for('page_main.page_main'))