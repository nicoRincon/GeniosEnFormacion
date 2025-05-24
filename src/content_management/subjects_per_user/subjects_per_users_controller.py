from src.content_management.subjects_per_user.subjects_per_users_service import SubjectsPerUsersService
from src.db_connection import app
from flask import redirect, render_template, url_for, request, session

@app.route("/subjects_per_login", methods=["GET"])
def subjects_per_login():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    subjects_to_show = []
    try:
        subjects = SubjectsPerUsersService().get_subjects_per_user()
        for subject in subjects:
            subjects_to_show.append({
                'id': subject.id,
                'subject_name': subject.nombre,
                'description': subject.descripcion
            })
    except ValueError as e:
        error = str(e.__str__())

    return render_template(
        'content_management/subjects_per_login.html',
        subjects=subjects_to_show,
        error=error,
        message=message
    )

@app.route("/subjects/<int:subject_id>/user", methods=["POST"])
def set_subjects_per_login(subject_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    try:
        SubjectsPerUsersService().set_subjects_per_user(subject_id)
        message = "Materia asignada."
    except ValueError as e:
        error = str(e.__str__())

    return url_for('subjects_per_login', message=message, error=error)