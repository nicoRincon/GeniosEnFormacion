from flask import redirect, render_template, url_for, request, session
from src.pages.pages_by_users_service import PagesByUsers
from src.login.login import User
from src.db_connection import app

import src.users.roles_controller


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    error = request.args.get('error', None)

    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        pages_by_users = PagesByUsers().get_page_by_user_id(session['user_id'])
    except ValueError as e:
        error = str(e.__str__())
        pages_by_users = []

    session['pages_by_users'] = pages_by_users

    return render_template(
        'dashboard.html',
        error=error
    )


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = request.args.get('error', None)
    tab = request.args.get('tab', 'login')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == '' or password == '':
            error = 'Por favor, ingrese su nombre de usuario y contraseña.'
            return render_template("login.html", error=error)

        try:
            User(username, password).login()
            return redirect(url_for('dashboard'))
        except ValueError as e:
            error = str(e.__str__())

    return render_template("login.html", error=error, tab=tab)

@app.route("/register", methods=["POST", "GET"])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username_register']
        name = request.form['name_register']
        last_name = request.form['lastname_register']
        email = request.form['email_register']
        password = request.form['password_register']
        confirm_password = request.form['confirm_password_register']
        try:
            User( username, password, confirm_password, name, last_name, email).register()
            return redirect(url_for('login'))
        except ValueError as e:
            error = str(e.__str__())

    return redirect(url_for('login', error=error, tab='register'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    User(session['username'], '').logout()
    return redirect(url_for('login'))

@app.route('/business_understanding', methods=['GET'])
def business_understanding():
    return render_template('project_explanation/business_understanding.html', username=session['username'])

@app.route('/data_engineering', methods=['GET'])
def data_engineering():
    return render_template('project_explanation/data_engineering.html', username=session['username'])

@app.route('/model_engineering', methods=['GET'])
def model_engineering():
    return render_template('project_explanation/model_engineering.html', username=session['username'])

@app.route('/model_evaluation', methods=['GET'])
def model_evaluation():
    return render_template('project_explanation/model_evaluation.html', username=session['username'])

@app.route('/model_deployment', methods=['GET'])
def model_deployment():
    return render_template('project_explanation/model_deployment.html', username=session['username'])


@app.context_processor
def inject_pages_by_users():
    return {
        "pages_by_users": session.get("pages_by_users", []),
        "username": session.get("username", None),
    }
