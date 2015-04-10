from flask import render_template, Blueprint

import views.api as api
import tools


app = Blueprint('page_scoreboard', __name__)

@app.route('/scoreboard', methods=['GET', 'POST'])
@tools.pages.page('scoreboard')
def page_scoreboard():
    return render_template('scoreboard.html', teams=api.stats.scoreboard()['data'])