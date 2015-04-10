# Not implemented yet
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
        return tools.api.gen_result_fail('min_score not an integer')
    return tools.api.gen_result_success({'count': tools.db.get_team_count(min_score)})

@app.route('/api/stats/team_count', methods=['GET', 'POST'])
@tools.api.response
def public_team_count():
    return team_count(**tools.general.unpack_request_data(**(request.args if request.method == 'GET' else request.form)))

def get_score_data(**params):
    params_check = tools.api.check_params(['team'], **params)
    if not params_check['success']:
        return params_check['result']
    team = tools.db.get_team_from_name(params['team'])
    if team is None:
        return tools.api.gen_result_fail('Team does not exist!')
    tools.db.refresh_score(team['_id'])
    result = OrderedDict()
    solved_problems = []
    for i in xrange(len(problems.problems)):
        if problems.problems[i]['enabled'] and str(problems.problems[i]['id']) in team['solved_problems'] and \
                team['solved_problems'][str(problems.problems[i]['id'])]:
            solved_problems.append(problems.problems[i]['name'])
    result['score'] = team['score']
    result['solved'] = solved_problems
    return tools.api.gen_result_success(result)

@app.route('/api/stats/get_score_data', methods=['GET', 'POST'])
@tools.api.response
def public_get_score_data():
    return get_score_data(**tools.general.unpack_request_data(**(request.args if request.method == 'GET' else request.form)))