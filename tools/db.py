from collections import OrderedDict

from flask import current_app
from pymongo import MongoClient
from bson.objectid import ObjectId

import config
from database import problems


def open_database():
    return MongoClient('localhost', 27017)[config.db.DATABASE_NAME]

def open_collection(collection, database=None):
    if database is None:
        database = current_app.db
    return database[collection]

class User:
    def __init__(self, user):
        self.authenticated = True
        self.active = True
        self.anonymous = False
        self.id = str(user['_id'])
        self.type = user['type']
        self.name = user['name']
        self.email = user['email']
        self.username = user['username']
        self.password = user['password']
        self.teams = user['teams']

    def __eq__(self, other):
        return self.id == other.get_id()

    def __ne__(self, other):
        return self.id != other.get_id()

    def is_authenticated(self):
        return self.authenticated

    def set_authenticated(self, value):
        self.authenticated = value

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return self.id

    def get_team(self):
        if config.platform.CTF_NAME in self.teams:
            return self.teams[config.platform.CTF_NAME]
        return None

def load_user(id):
    users = open_collection('users')
    user = users.find_one({'_id': ObjectId(id)})
    if user is not None:
        return User(user)
    else:
        return None

def get_user(user_id):
    return open_collection('users').find_one({'_id': ObjectId(user_id)})

# Identifier can be email or username
def load_user_from_identifier(identifier):
    users = open_collection('users')
    found = users.find({'username': identifier}).limit(1)
    if found.count() > 0:
        return User(found[0])
    found = users.find({'email': identifier}).limit(1)
    if found.count() > 0:
        return User(found[0])
    return None

def refresh_score(team_id, db=None):
    teams = open_collection('teams', database=db)
    team = teams.find_one({'_id': team_id})
    original_score = team['score']
    score = 0
    for (problem_id, problem_solved) in dict(team['solved_problems']).iteritems():
        if team['solved_problems'][problem_id] and get_problem(int(problem_id))['enabled']:
            score += get_problem(int(problem_id))['value']
    if score != original_score:
        teams.update({'_id': team_id}, {'$set': {'score': score}})

def get_team_from_name(name):
    return open_collection('teams').find_one({'name': name})

def get_team_id_from_name(name):
    team = get_team_from_name(name)
    if team is None:
        return None
    else:
        return team['_id']

def get_team(team_id):
    return open_collection('teams').find_one({'_id': team_id})

def get_scores_list():
    teams_collection = open_collection('teams')
    teams = []
    for team in teams_collection.find():
        teams.append((team['name'], team['score'], team['last_solve_time']))
    teams = sorted(teams, key=lambda x: (-x[1], x[2]))
    result = []
    for team in teams:
        team_info = OrderedDict()
        team_info['name'] = team[0]
        team_info['score'] = team[1]
        team_info['last_solve_time'] = team[2]
        result.append(team_info)
    return result

def get_team_count(min_score=0):
    return open_collection('teams').find({'score': {'$gte': min_score}}).count()

def get_problem(problem_id):
    for problem in problems.problems:
        if problem['id'] == problem_id:
            return problem
    # Someone killed the problem
    return {'enabled': False}

def refresh_all_scores(db=None):
    for team in open_collection('teams', database=db).find():
        refresh_score(team['_id'], db=db)