from flask import Blueprint

import tools
import api
import redirect
import pages


app = Blueprint('views', __name__)
to_register = tools.general.get_reg_list([api, pages, redirect])