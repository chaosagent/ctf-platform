from collections import OrderedDict
from functools import wraps
import json

from flask import Response

import tools




# Decorator for api_response
# Apparently flask needs unique function names, so this is temporarily disabled.
def response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return api_response(func(*args, **kwargs))
    return wrapper

def to_json(dict, pretty=False):
    return json.dumps(dict) if not pretty else json.dumps(dict, indent=4, separators=(',', ': '))

def api_response(result, pretty=True):
    return Response(to_json(result, pretty=pretty), mimetype="application/json")

def gen_result_missing_param(params):
    missingparamsstring = ', '.join(params)
    return gen_result_fail('Missing parameters: ' + missingparamsstring)

def gen_result_success(data=None):
    result = OrderedDict([
        ('success', True)])
    if type(data) == str:
        result['message'] = data
    elif data is not None:
        result['data'] = data
    return result

def gen_result_fail(message=None):
    result = OrderedDict([
        ('success', False)])
    if message is not None:
        result['message'] = message
    return result

def gen_result_unavailable():
    return gen_result_fail('API call unavailable')

def gen_result_unauthorized():
    return gen_result_fail('You are not logged in')

def check_params(reqparams, **kwargs):
    missing_params = []
    for param in reqparams:
        if param not in kwargs:
            missing_params.append(param)
    if len(missing_params) > 0:
        return {
            'success': False,
            'result': gen_result_missing_param(missing_params)
        }
    return {'success': True}

def is_valid_username(username):
    return tools.general.remove_from_string(username, ['.', '-', '_']).isalnum()