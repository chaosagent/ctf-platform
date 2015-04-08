from flask import render_template, Blueprint
from flask_login import current_user

import tools

import views.api as api
import config


app = Blueprint('page_problems', __name__)

@app.route('/problems', methods=['GET', 'POST'])
@tools.accounts.login_required_if(not config.platform.PROBLEMS_AVAILABLE_WITHOUT_LOGIN)
def page_problems():
    return render_template('problems.html', problems=api.problems.get_all_problems(),
                           use_hints=config.platform.USE_HINTS,
                           user_authenticated=current_user.is_authenticated(),
                           user_in_team=(current_user.is_authenticated() and current_user.get_team() is not None))