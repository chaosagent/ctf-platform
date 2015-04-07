# Not implemented yet
# TODO: Implement scoreboard

from flask import Blueprint

import tools

app = Blueprint('api_stats', __name__)

def scoreboard():
    return tools.api.gen_result_success(tools.db.get_scores_list())

@app.route('/api/stats/scoreboard', methods=['GET', 'POST'])
@tools.api.response
def public_scoreboard():
    return scoreboard()