

from src.db_connection import app
from flask import redirect, render_template, url_for, request, session
from src.users.roles_service import Roles
from flask import jsonify

@app.route("/roles", methods=["POST"])
def create_role():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = None
    message = None
    if request.method == 'POST':
        role_name = request.form['role_name']
        try:
            message = Roles().create_role(role_name)
        except ValueError as e:
            error = str(e.__str__())

    return redirect(url_for('roles', error=error, message=message))

@app.route("/roles", methods=["GET"])
def roles():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    all_roles = Roles().get_all_roles()

    return render_template('users/roles.html', all_roles=all_roles, error=error, message=message)

@app.route("/roles/<int:role_id>", methods=["GET", "POST"])
def role_by_id(role_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    role = None

    method = request.form.get('_method', 'GET')
    if method == 'PATCH':
        return edit_role(role_id)
    elif method == 'DELETE':
        return delete_role(role_id)

    if request.method == 'GET' or method == 'GET':
        role = Roles().get_role_by_id(role_id)

    return jsonify({ 'id': role.id, 'role_name': role.nombre_rol }) if role else None

def edit_role(role_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        role_name = request.form['edit_rol_name']
        message = Roles().update_role(role_id, role_name).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('roles', error=error, message=message))

def delete_role(role_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))
    error = None
    message = None
    try:
        message = Roles().delete_role(role_id).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('roles', error=error, message=message))
