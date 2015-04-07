from flask import Blueprint, request
from flask import redirect as redirect_user


app = Blueprint('redirect', __name__)

@app.route('/redirect', methods=['GET', 'POST'])
def redirect():
    return redirect_user(request.args['next'])