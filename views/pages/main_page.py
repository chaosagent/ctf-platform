from flask import render_template, Blueprint

import views.api as api

app = Blueprint('page_main', __name__)

@app.route('/', methods=['GET', 'POST'])
def page_login():
    return render_template('main_page.html', team_count=str(api.stats.team_count(0)['data']['count']))