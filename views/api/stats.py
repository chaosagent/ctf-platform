# Not implemented yet
# TODO: Implement scoreboard

from flask import Blueprint, request

import tools

app = Blueprint('api_stats', __name__)

def scoreboard():
    return tools.api.gen_result_success(tools.db.get_scores_list())

@app.route('/api/stats/scoreboard', methods=['GET', 'POST'])
@tools.api.response
def public_scoreboard():
    return scoreboard()

def team_count(min_score=0):
    try:
        min_score = int(min_score)
    except ValueError:
        return tools.api.gen_result_fail('ID not an integer')
    return tools.api.gen_result_success({'count': tools.db.get_team_count(min_score)})

@app.route('/api/stats/team_count', methods=['GET', 'POST'])
@tools.api.response
def public_team_count():
    return team_count(**tools.general.unpack_request_data(**(request.args if request.method == 'GET' else request.form)))