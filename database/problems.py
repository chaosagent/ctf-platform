def add_ids(items):
    result = []
    i = 0
    for item in items:
        item['id'] = i
        result.append(item)
        i += 1
    return result

problems = [
    {
        'id': 0,
        'enabled': True,
        'name': 'Test',
        'value': 5,
        'statement': 'What is 1 + 1?',
        'hint': 'Simple (not) arithmetic.',
        'solution': 'TwO'
    },
    {
        'id': 1,
        'enabled': True,
        'name': 'l33t',
        'value': 10,
        'statement': 'What is my name, but more?',
        'hint': 'I am a problem',
        'solution': '1337'
    },
    {
        'id': 2,
        'enabled': True,
        'name': 'Advanced Math',
        'value': 15,
        'statement': 'What is 2 * 2?',
        'hint': 'Wow what does that asterisk mean.',
        'solution': '4'
    },
    {
        'id': 3,
        'enabled': True,
        'name': 'WHATISTHIS',
        'value': 20,
        'statement': 'If 3y = 2x and x = 3, what is y?',
        'hint': 'I don\'t know whats happening, but its scary.',
        'solution': '2'
    }
]
problems = sorted(problems, key=lambda x: x['id'])