from flask import render_template, Blueprint

app = Blueprint('page_register', __name__)

@app.route('/register', methods=['GET', 'POST'])
def page_register():
    return render_template('register.html')