import time

from flask import Blueprint, request

from flask_login import login_user, login_required, logout_user, current_user
from bson.objectid import ObjectId

import config
import tools


app = Blueprint('api_accounts', __name__)

def register(**params):
    if not config.platform.CTF_STANDALONE:
        return tools.api.gen_result_unavailable()
    params_check = tools.api.check_params(['type', 'email', 'name', 'username', 'password'], **params)
    if not params_check['success']:
        return params_check['result']
    users = tools.db.open_collection('users')
    duplicates = tools.general.check_for_duplicates(users, email=params['email'], username=params['username'])
    if len(duplicates) > 0:
        return tools.api.gen_result_fail('Duplicate parameters: ' + ', '.join(duplicates))
    if not tools.api.is_valid_username(params['username']):
        return tools.api.gen_result_fail('Invalid username')
    if params['email'].find('@') == -1:
        return tools.api.gen_result_fail('Invalid email address')
    user = tools.general.get_dictionary_items(params, ['type', 'email', 'name', 'username'])
    # Use username as salt; ':' as separator
    hashed_password = tools.general.sha512(params['password'], params['username'])
    user['password'] = ':'.join(hashed_password)
    # user.update({'_id': users.find().sort('_id', pymongo.DESCENDING).limit(1)[0]['_id'] + 1 if users.find().count() != 0 else 0})
    user['teams'] = {}
    users.insert(user)
    user_id = str(users.find_one({'email': params['email']})['_id'])
    result = {
        'user_id': user_id
    }
    return tools.api.gen_result_success(result)

@app.route('/api/accounts/register', methods=['POST'])
@tools.api.response
def public_register():
    return register(**tools.general.unpack_request_data(**request.form))

def register_team(user_id, **params):
    params_check = tools.api.check_params(['name'], **params)
    if not params_check['success']:
        return params_check['result']
    user = tools.db.load_user(user_id)
    if user.get_team() is not None:
        return tools.api.gen_result_fail('User already in team!')
    teams = tools.db.open_collection('teams')
    duplicates = tools.general.check_for_duplicates(teams, name=params['name'])
    if len(duplicates) > 0:
        return tools.api.gen_result_fail('Team already exists!')
    # team shares id with user who created it
    teams.insert({
        '_id': user_id,
        'name': params['name'],
        'members': [
            user_id
        ],
        'score': 0,
        'last_solve_time': time.time(),
        'solved_problems': {}
    })
    users = tools.db.open_collection('users')
    users.update({'_id': ObjectId(user_id)}, {'$set': {'teams.%s' % config.platform.CTF_NAME: user_id}})
    return tools.api.gen_result_success({'team_id': user_id})

@app.route('/api/accounts/register_team', methods=['POST'])
@login_required
@tools.api.response
def public_register_team():
    return register_team(current_user.id, **tools.general.unpack_request_data(**request.form))

def join_team(user_id, **params):
    params_check = tools.api.check_params(['name'], **params)
    if not params_check['success']:
        return params_check['result']
    team_id = tools.db.get_team_id_from_name(params['name'])
    if team_id is None:
        return tools.api.gen_result_fail('Team does not exist!')
    users = tools.db.open_collection('users')
    user = tools.db.get_user(user_id)
    if config.platform.CTF_NAME in user['teams'] and user['teams'][config.platform.CTF_NAME] is not None:
        return tools.api.gen_result_fail('User already in team!')
    teams = tools.db.open_collection('teams')
    target_team = tools.db.get_team(team_id)
    if target_team is None:
        return tools.api.gen_result_fail('Team does not exist!')
    if len(target_team['members']) >= config.platform.MAX_TEAM_SIZE:
        return tools.api.gen_result_fail('Team full!')
    teams.update({'_id': team_id}, {'$push': {'members': user_id}})
    users.update({'_id': ObjectId(user_id)}, {'$set': {'teams.%s' % config.platform.CTF_NAME: team_id}})
    return tools.api.gen_result_success({'team_id': team_id})

@app.route('/api/accounts/join_team', methods=['POST'])
@login_required
@tools.api.response
def public_join_team():
    return join_team(current_user.id, **tools.general.unpack_request_data(**request.form))

def login(**params):
    params_check = tools.api.check_params(['identifier', 'password'], **params)
    if not params_check['success']:
        return params_check['result']
    user = tools.db.load_user_from_identifier(params['identifier'])
    if user is None:
        return tools.api.gen_result_fail('Email/username not found')
    if user.password == ':'.join(tools.general.sha512(params['password'], user.username)):
        login_user(user)
        return tools.api.gen_result_success(message='Logged in!')
    else:
        return tools.api.gen_result_fail('Incorrect password')

@app.route('/api/accounts/login', methods=['POST'])
@tools.api.response
def public_login():
    return login(**tools.general.unpack_request_data(**request.form))

def logout():
    logout_user()
    return tools.api.gen_result_success(message='Logged out.')

@app.route('/api/accounts/logout', methods=['GET', 'POST'])
@login_required
@tools.api.response
def public_logout():
    return logout()