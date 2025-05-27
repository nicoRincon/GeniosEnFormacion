from src.content_management.subjects.subject_service import SubjectsService
from src.content_management.subjects_per_user.subjects_per_users_service import SubjectsPerUsersService
from src.db_connection import app
from flask import jsonify, redirect, render_template, url_for, request, session

@app.route("/subjects_per_login", methods=["GET"])
def subjects_per_login():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    subjects_to_show = []
    try:
        subjects = SubjectsService().get_all_subjects()
        selection_subjects = [{
            'id': subject.id,
            'name': subject.nombre,
        } for subject in subjects]

        subjects_per_login = SubjectsPerUsersService().get_all_subjects_per_user()
        for subject in subjects_per_login:
            subjects_to_show.append({
                'assignment_id': subject.id_asignacion,
                'subject_id': subject.id,
                'subject_name': subject.nombre,
                'description': subject.descripcion,
                'username': subject.nombre_usuario,
            })
    except ValueError as e:
        error = str(e.__str__())

    return render_template(
        'content_management/subjects_per_login.html',
        assignments=subjects_to_show,
        error=error,
        message=message,
        selection_subjects=selection_subjects
    )

@app.route("/subjects/<int:subject_id>/user", methods=["POST"])
def set_subjects_per_login(subject_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    assignment_id = None
    try:
        assignment_id = SubjectsPerUsersService().set_subjects_per_user(subject_id)
        message = "Materia asignada."
    except ValueError as e:
        error = str(e.__str__())

    return jsonify({ 'message':message, 'error':error, 'assignment_id':assignment_id })

@app.route("/subjects_per_login/<int:assignment_id>", methods=["DELETE"])
def delete_assignment_by_id(assignment_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    try:
        SubjectsPerUsersService().delete_assignment_by_id(assignment_id)
        message = "Materia eliminada."
    except ValueError as e:
        error = str(e.__str__())

    return jsonify({ "message": message, "error": error })