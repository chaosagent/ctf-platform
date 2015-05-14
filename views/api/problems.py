from collections import OrderedDict
import time

from flask import Blueprint, request
from flask_login import login_required, current_user

import config.platform as config
import tools
from database import problems


app = Blueprint('api_problems', __name__)

@tools.api.competition_started_required
def get_problem(problem_id):
    try:
        problem_id = int(problem_id)
    except ValueError:
        return tools.api.gen_result_fail('ID not an integer')
    problem = tools.db.get_problem(problem_id)
    if problem is None:
        return tools.api.gen_result_fail('Invalid problem ID')
    if not problem['enabled']:
        return tools.api.gen_result_fail('Problem disabled')
    result = OrderedDict([
        ('id', problem['id']),
        ('name', problem['name']),
        ('value', problem['value']),
        ('statement', problem['statement'])
    ])
    if config.USE_HINTS:
        result['hint'] = problem['hint']
    return tools.api.gen_result_success(result)

@tools.api.competition_started_required
def get_all_problems():
    result = []
    for problem in problems.problems:
        if not problem['enabled']:
            continue
        filtered_problem = OrderedDict({
            ('id', problem['id']),
            ('name', problem['name']),
            ('value', problem['value']),
            ('statement', problem['statement'])
        })
        if config.USE_HINTS:
            filtered_problem['hint'] = problem['hint']
        result.append(filtered_problem)
    return tools.api.gen_result_success(result)

@app.route('/api/problems/get', methods=['GET', 'POST'])
@tools.api.response
def public_get_problem():
    if 'problem_id' in request.args:
        return get_problem(request.args['problem_id'] if request.method == 'GET' else request.form['problem_id'])
    else:
        return get_all_problems()

@tools.api.competition_active_required
def submit_solution(team_id, **params):
    params_check = tools.api.check_params(['problem_id', 'flag'], **params)
    if not params_check['success']:
        return params_check['result']
    problem_id = params['problem_id']
    try:
        problem_id = int(problem_id)
    except ValueError:
        return tools.api.gen_result_fail('ID not an integer')
    problem = tools.db.get_problem(problem_id)
    if problem is None:
        return tools.api.gen_result_fail('Invalid problem ID')
    if not problem['enabled']:
        return tools.api.gen_result_fail('Problem disabled')
    if team_id is None:
        return tools.api.gen_result_fail('User is not in a team!')
    submitted_flag = params['flag']
    result = OrderedDict()
    if tools.general.check_solution(submitted_flag, problem['solution']):
        result['correct'] = True
        teams = tools.db.open_collection('teams')
        solved = tools.db.get_team(team_id)['solved_problems']
        if str(problem_id) in solved and solved[str(problem_id)]:
            result['points_awarded'] = 0
            result['message'] = config.MESSAGE_ALREADY_SOLVED
        else:
            current_time = time.time()
            teams.update({'_id': team_id}, {'$set': {'last_solve_time': current_time,
                                                     'solved_problems.%s.solved' % str(problem_id): True,
                                                     'solved_problems.%s.solved_time' % str(problem_id): current_time}})
            tools.db.refresh_score(team_id)
            result['points_awarded'] = problem['value']
            result['message'] = config.MESSAGE_CORRECT_ANSWER
    else:
        result['correct'] = False
        result['points_awarded'] = 0
        result['message'] = config.MESSAGE_INCORRECT_ANSWER
    return tools.api.gen_result_success(result)

@app.route('/api/problems/submit', methods=['POST'])
@login_required
@tools.api.response
def public_submit_solution():
    return submit_solution(current_user.get_team(), **tools.general.unpack_request_data(**request.form))

@tools.api.competition_started_required
def is_solved(**params):
    params_check = tools.api.check_params(['team', 'problem_id'], **params)
    if not params_check['success']:
        return params_check['result']
    team, problem_id = tools.db.get_team_from_name(params['team']), params['problem_id']
    if team is None:
        return tools.api.gen_result_fail('Team does not exist!')
    if not tools.general.is_int(problem_id):
        return tools.api.gen_result_fail('ID not an integer')
    problem = tools.db.get_problem(int(problem_id))
    if problem is None:
        return tools.api.gen_result_fail('Invalid problem ID')
    if not problem['enabled']:
        return tools.api.gen_result_fail('Problem disabled')
    solved = team['solved_problems']
    result = {}
    if problem_id in solved and solved[problem_id]:
        result['solved'] = True
    else:
        result['solved'] = False
    return tools.api.gen_result_success(result)

@app.route('/api/problems/is_solved', methods=['GET', 'POST'])
@tools.api.response
def public_is_solved():
    return is_solved(**tools.general.unpack_request_data(**(request.args if request.method == 'GET' else request.form)))