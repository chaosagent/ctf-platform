from flask import Blueprint

import tools
import login
import scoreboard


app = Blueprint('pages', __name__)
to_register = tools.general.get_reg_list([login, scoreboard])