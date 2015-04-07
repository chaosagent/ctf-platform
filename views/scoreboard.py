from flask import render_template, Blueprint

import views.api as api


app = Blueprint('page_scoreboard', __name__)

@app.route('/scoreboard')
def page_scoreboard():
    return render_template('scoreboard.html', teams=api.stats.scoreboard()['data'])