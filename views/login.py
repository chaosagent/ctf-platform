from flask import render_template, Blueprint

app = Blueprint('page_login', __name__)

@app.route('/login', methods=['GET', 'POST'])
def page_login():
    return render_template('login.html')