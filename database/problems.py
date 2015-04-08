def add_ids(items):
    result = []
    i = 0
    for item in items:
        item['id'] = i
        result.append(item)
        i += 1
    return result

problems = add_ids([
    {
        'enabled': True,
        'name': 'Test',
        'value': 5,
        'statement': 'What is 1 + 1?',
        'hint': 'Simple arithmetic.',
        'solution': 'TwO'
    },
    {
        'enabled': True,
        'name': 'l33t',
        'value': 10,
        'statement': 'What is my name, but more?',
        'hint': 'I am a problem',
        'solution': '1337'
    }
])
problems = sorted(problems, key=lambda x: x['id'])