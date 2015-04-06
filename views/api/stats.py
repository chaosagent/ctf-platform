# Not implemented yet
# TODO: Implement scoreboard

import tools


def scoreboard():
    solved_colls = tools.db.open_collection('solved').find()
    # Solo scores for now
    teams = []
    for coll in solved_colls:
        teams.append(())