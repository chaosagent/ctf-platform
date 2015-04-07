# Not implemented yet
# TODO: Implement scoreboard
from collections import OrderedDict

from flask import Blueprint, request

from database import problems

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

def get_score_data(team_id):
    if team_id is None:
        return tools.api.gen_result_fail('Team does not exist!')
    tools.db.refresh_score(team_id)
    team = tools.db.get_team(team_id)
    result = OrderedDict()
    solved_problems = []
    for i in xrange(len(problems.problems)):
        if str(i) in team['solved_problems'] and team['solved_problems'][str(i)]:
            solved_problems.append(problems.problems[i]['name'])
    result['score'] = team['score']
    result['solved'] = solved_problems
    return tools.api.gen_result_success(result)

@app.route('/api/stats/get_score_data/<name>', methods=['GET', 'POST'])
@tools.api.response
def public_get_score_data(name):
    return get_score_data(tools.db.get_team_id_from_name(name))