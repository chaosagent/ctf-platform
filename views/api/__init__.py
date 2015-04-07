from flask import Blueprint

import tools
import general
import problems
import accounts
import stats

app = Blueprint('api', __name__)
to_register = tools.general.get_reg_list([general, problems, accounts, stats])