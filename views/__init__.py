from flask import Blueprint

import tools
import api
import scoreboard
import login


app = Blueprint('views', __name__)
to_register = tools.general.get_reg_list([api, scoreboard, login])