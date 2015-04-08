from flask import Blueprint, redirect, url_for

import views.api as api

app = Blueprint('page_logout', __name__)

# Redirect even if not logged in already
@app.route('/logout', methods=['GET', 'POST'])
def page_logout():
    api.accounts.logout()
    return redirect(url_for('page_main.page_main'))