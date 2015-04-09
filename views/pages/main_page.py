from flask import render_template, Blueprint

import views.api as api
import tools

app = Blueprint('page_main', __name__)

@app.route('/', methods=['GET', 'POST'])
@tools.pages.page
def page_main():
    return render_template('main_page.html', team_count=str(api.stats.team_count(0)['data']['count']))