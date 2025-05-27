from src.content_management.subjects.subject_service import SubjectsService
from database.Materias.Tema import Tema
from src.db_connection import app
from flask import redirect, render_template, url_for, request, session
from src.content_management.topics.topics_service import TopicsService
from flask import jsonify

@app.route("/topics", methods=["POST"])
def create_topic():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    if request.method == 'POST':
        topic_name = request.form['topic_name']
        topic_description = request.form['topic_description']
        subject_id = request.form['subject_id']
        try:
            message = TopicsService().create_topic(
                subject_id,
                topic_name,
                topic_description
            ).get('message', None)
        except ValueError as e:
            error = str(e.__str__())

    return redirect(url_for('topics', error=error, message=message))

@app.route("/topics", methods=["GET"])
def topics():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    topics_to_show = []
    try:
        all_topics = TopicsService().get_all_topics()
        for topic in all_topics:
            topics_to_show.append({
                'id': topic.id,
                'subject_name': topic.nombre_materia,
                'topic_name': topic.nombre,
                'description': topic.descripcion
            })

        subjects = SubjectsService().get_all_subjects()
        selection_subjects = [
            {
                'id': subject.id,
                'name': subject.nombre,
            } for subject in subjects
        ]
    except ValueError as e:
        error = str(e.__str__())

    return render_template(
        'content_management/topics.html',
        topics=topics_to_show,
        error=error,
        message=message,
        selection_subjects=selection_subjects
    )

@app.route("/topics/<int:topic_id>", methods=["GET", "POST"])
def topic_by_id(topic_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    topic: Tema|None = None

    method = request.form.get('_method', 'GET')
    if method == 'PATCH':
        return edit_topic(topic_id)
    elif method == 'DELETE':
        return delete_topic(topic_id)

    if request.method == 'GET' or method == 'GET':
        topic = TopicsService().get_topic_by_id(topic_id)

    return jsonify({
        'id': topic.id,
        'subject_id': topic.id_materia,
        'topic_name': topic.nombre,
        'topic_description': topic.descripcion
    }) if topic else None

def edit_topic(topic_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        topic_name = request.form['edit_topic_name']
        topic_description = request.form['edit_topic_description']
        subject_id = request.form['edit_subject_id']
        message = TopicsService().update_topic(
            topic_id, subject_id, topic_name, topic_description
        ).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('topics', error=error, message=message))

def delete_topic(topic_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        message = TopicsService().delete_topic(topic_id).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('topics', error=error, message=message))
