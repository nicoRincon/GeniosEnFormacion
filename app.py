from flask import Flask, redirect, render_template, url_for, request, session
from src.login.login import User

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            User(username, password).login()
            return redirect(url_for('dashboard'))
        except ValueError as e:
            error = str(e.__str__())

    return render_template("login.html", error=error)

@app.route("/register", methods=["POST", "GET"])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username_register']
        password = request.form['password_register']
        confirm_password = request.form['confirm_password_register']
        try:
            User(username, password, confirm_password).register()
            return redirect(url_for('login'))
        except ValueError as e:
            error = str(e.__str__())

    return render_template('signup.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    User(session['username'], '').logout()
    return redirect(url_for('login'))
