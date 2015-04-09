import hashlib
import time

import config


def get_dictionary_items(dict, items):
    result = {}
    for item in items:
        result.update({item: dict[item]})
    return result

def get_reg_list(to_scan):
    result = [] + to_scan
    for module in to_scan:
        if hasattr(module, 'to_register'):
            result += module.to_register
    return result

def check_for_duplicates(collection, **items):
    duplicates = []
    for (key, value) in items.iteritems():
        if collection.find({key: value}).count() > 0:
            duplicates.append(key)
    return duplicates

def sha512(string, salt):
    return [hashlib.sha512(string + salt).hexdigest(), salt]

def remove_from_string(string, to_remove):
    result = ''
    for c in string:
        if c not in to_remove:
            result += c
    return result

def unpack_request_data(**kwargs):
    result = {}
    for (key, value) in kwargs.iteritems():
        result[key] = value[0]
    return result

def is_int(string):
    try:
        int(string)
    except ValueError:
        return False
    return True

def check_solution(submitted, answer):
    return remove_from_string(submitted.lower(), [' ']) == remove_from_string(answer.lower(), [' '])

def competition_state():
    if time.time() < config.platform.COMPETITION_START_TIME:
        return -1
    elif time.time() <= config.platform.COMPETITION_END_TIME:
        return 0
    else:
        return 1

def competition_active():
    return competition_state() == 0

def competition_started():
    return competition_state() >= 0

def competition_ended():
    return competition_state() == 1