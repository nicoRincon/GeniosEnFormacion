from database.Materias.Materia import Materia
from src.db_connection import app
from flask import redirect, render_template, url_for, request, session
from src.content_management.subjects.subject_service import SubjectsService
from flask import jsonify

@app.route("/subjects", methods=["POST"])
def create_subject():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        subject_description = request.form['subject_description']
        try:
            message = SubjectsService().create_subject(subject_name, subject_description)
        except ValueError as e:
            error = str(e.__str__())

    return redirect(url_for('subjects', error=error, message=message))

@app.route("/subjects", methods=["GET"])
def subjects():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    subjects_to_show = []
    try:
        all_subjects = SubjectsService().get_all_subjects()
        for subject in all_subjects:
            subjects_to_show.append({
                'id': subject.id,
                'subject_name': subject.nombre,
                'description': subject.descripcion
            })
    except ValueError as e:
        error = str(e.__str__())
        all_subjects = []

    return render_template(
        'content_management/subjects.html',
        subjects=subjects_to_show,
        error=error,
        message=message
    )

@app.route("/subjects/<int:subject_id>", methods=["GET", "POST"])
def subject_by_id(subject_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    subject: Materia|None = None

    method = request.form.get('_method', 'GET')
    if method == 'PATCH':
        return edit_subject(subject_id)
    elif method == 'DELETE':
        return delete_subject(subject_id)

    if request.method == 'GET' or method == 'GET':
        subject = SubjectsService().get_subject_by_id(subject_id)

    return jsonify({
        'id': subject.id,
        'subject_name': subject.nombre,
        'subject_description': subject.descripcion
    }) if subject else None

def edit_subject(subject_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        subject_name = request.form['edit_subject_name']
        subject_description = request.form['edit_subject_description']
        message = SubjectsService().update_subject(
            subject_id, subject_name, subject_description
        ).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('subjects', error=error, message=message))

def delete_subject(subject_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        message = SubjectsService().delete_subject(subject_id).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('subjects', error=error, message=message))
