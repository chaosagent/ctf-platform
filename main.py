import sys
import os
import argparse

import jinja2

from flask import Flask
from flask_login import LoginManager

import config
import tools
import views


sys.path.insert(0, os.path.realpath(__file__))

app = Flask(__name__)
app.config.from_object(config.flask)

args = None

def wipe_database():
    tools.db.db.drop_collection('users')
    tools.db.db.drop_collection('teams')
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
    login_manager.unauthorized_handler(views.api.accounts.public_not_logged_in)
    login_manager.login_view = 'api_accounts.public_login'

def set_up_jinja_loader():
    my_loader = jinja2.FileSystemLoader('frontend/templates')
    app.jinja_loader = my_loader

def handle_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False,
                        help='Use Flask debug mode')
    parser.add_argument('--wipe-db', dest='wipe_db', action='store_const', const=True, default=False,
                        help='Wipe database on startup')
    global args
    args = parser.parse_args()


if __name__ == '__main__':
    handle_args()
    if args.wipe_db:
        wipe_database()
    if args.debug:
        app.debug = True
    register_blueprints()
    set_up_login_manager()
    set_up_jinja_loader()
    app.run(host='0.0.0.0')