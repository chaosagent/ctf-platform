import sys
import os
import argparse

from flask import Flask
from flask_login import LoginManager

import config
import tools


sys.path.insert(0, os.path.realpath(__file__))

app = Flask(__name__)
app.config.from_object(config.flask)

args = None

db = tools.db.open_database()

def set_up_db():
    tools.db.refresh_all_scores(db=db)
    app.db = db

def wipe_database():
    db.drop_collection('users')
    db.db.drop_collection('teams')
    pass

def register_blueprints():
    import views
    to_register = tools.general.get_reg_list([views])
    for module in to_register:
        app.register_blueprint(module.app)

def set_up_login_manager():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(tools.db.load_user)
    login_manager.login_view = 'api_accounts.public_login'
    login_manager.unauthorized_handler(tools.general.public_not_logged_in)

def handle_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False,
                        help='Use Flask debug mode')
    parser.add_argument('--wipe-db', dest='wipe_db', action='store_const', const=True, default=False,
                        help='Wipe database on startup')
    global args
    args = parser.parse_args()

def set_up_jinja():
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

if __name__ == '__main__':
    handle_args()
    set_up_db()
    if args.wipe_db:
        wipe_database()
    if args.debug:
        app.debug = True
    register_blueprints()
    set_up_login_manager()
    set_up_jinja()
    app.run(host='0.0.0.0')