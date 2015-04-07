from collections import OrderedDict

from flask import Blueprint, request
from flask_login import login_required, current_user

import config.platform as config
import tools
from database import problems


app = Blueprint('api_problems', __name__)

def get_problem(problem_id):
    try:
        problem_id = int(problem_id)
    except ValueError:
        return tools.api.gen_result_fail('ID not an integer')
    if problem_id > len(problems.problems) or problem_id < 0:
        return tools.api.gen_result_fail('Invalid problem ID')
    if not problems.problems[problem_id]['enabled']:
        return tools.api.gen_result_fail('Problem disabled')
    problem = problems.problems[problem_id]
    result = OrderedDict([
        ('name', problem['name']),
        ('value', problem['value']),
        ('statement', problem['statement'])
    ])
    if config.USE_HINTS:
        result['hint'] = problem['hint']
    return tools.api.gen_result_success(result)

@app.route('/api/problems/get/<problem_id>', methods=['GET', 'POST'])
@tools.api.response
def public_get_problem(problem_id):
    return get_problem(problem_id)

def submit_solution(team_id, problem_id, **kwargs):
    try:
        problem_id = int(problem_id)
    except ValueError:
        return tools.api.gen_result_fail('ID not an integer')
    if problem_id > len(problems.problems) or problem_id < 0:
        return tools.api.gen_result_fail('Invalid problem ID')
    if not problems.problems[problem_id]['enabled']:
        return tools.api.gen_result_fail('Problem disabled')
    if team_id is None:
        return tools.api.gen_result_fail('User is not in a team!')
    params_check = tools.api.check_params(['flag'], **kwargs)
    if not params_check['success']:
        return params_check['result']
    submitted_flag = kwargs['flag']
    problem = problems.problems[problem_id]
    result = OrderedDict()
    # Allow for spacing/case deviations
    if submitted_flag.lower().replace(' ', '') == problem['solution'].lower().replace(' ', ''):
        result['correct'] = True
        teams = tools.db.open_collection('teams')
        solved = tools.db.get_team(team_id)['solved_problems']
        if str(problem_id) in solved and solved[str(problem_id)]:
            result['message'] = config.MESSAGE_ALREADY_SOLVED
        else:
            teams.update({'_id': team_id}, {'$set': {'solved_problems.%s' % str(problem_id): True}})
            tools.db.refresh_score(team_id)
            result['message'] = config.MESSAGE_CORRECT_ANSWER
    else:
        result['correct'] = False
        result['message'] = config.MESSAGE_INCORRECT_ANSWER
    return tools.api.gen_result_success(result)

@app.route('/api/problems/submit/<problem_id>', methods=['POST'])
@login_required
@tools.api.response
def public_submit_solution(problem_id):
    return submit_solution(current_user.get_team(), problem_id, **tools.general.unpack_request_data(**request.form))

def is_solved(team_id, problem_id):
    if team_id is None:
        return tools.api.gen_result_fail('Team does not exist!')
    if tools.db.load_user(team_id) is None:
        return tools.api.gen_result_fail('User does not exist!')
    if not tools.general.is_int(problem_id):
        return tools.api.gen_result_fail('ID not an integer')
    if int(problem_id) > len(problems.problems) or int(problem_id) < 0:
        return tools.api.gen_result_fail('Invalid problem ID')
    if not problems.problems[int(problem_id)]['enabled']:
        return tools.api.gen_result_fail('Problem disabled')
    solved = tools.db.get_team(team_id)['solved_problems']
    result = {}
    if problem_id in solved and solved[problem_id]:
        result['solved'] = True
    else:
        result['solved'] = False
    return tools.api.gen_result_success(result)

@app.route('/api/problems/is_solved/<name>/<problem_id>', methods=['GET', 'POST'])
@tools.api.response
def public_is_solved(name, problem_id):
    return is_solved(tools.db.get_team_id_from_name(name), problem_id)