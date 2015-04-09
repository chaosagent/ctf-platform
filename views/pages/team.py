from flask import render_template, Blueprint

from flask_login import login_required, current_user

app = Blueprint('page_team', __name__)

@app.route('/team', methods=['GET', 'POST'])
@login_required
def page_team():
    if current_user.get_team() is None:
        return render_template('not_in_team.html')
    else:
        return render_template('team.html')