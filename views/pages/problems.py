from flask import render_template, Blueprint
from flask_login import login_required

import views.api as api
import config


app = Blueprint('page_problems', __name__)

@app.route('/problems', methods=['GET', 'POST'])
@login_required
def page_problems():
    return render_template('problems.html', problems=api.problems.get_all_problems(), use_hints=config.platform.USE_HINTS)