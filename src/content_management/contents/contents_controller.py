from src.content_management.topics.topics_service import TopicsService
from database.Materias.Contenido import Contenido
from src.db_connection import app
from flask import redirect, render_template, url_for, request, session
from src.content_management.contents.contents_service import ContentsService
from flask import jsonify

@app.route("/contents", methods=["POST"])
def create_content():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    if request.method == 'POST':
        content_name = request.form['content_name']
        content_description = request.form['content_description']
        grade_level = request.form['grade_level']
        topic_id = request.form['topic_id']
        try:
            message = ContentsService().create_content(
                topic_id,
                content_name,
                content_description,
                grade_level
            ).get('message', None)
        except ValueError as e:
            error = str(e.__str__())

    return redirect(url_for('contents', error=error, message=message))

@app.route("/contents", methods=["GET"])
def contents():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    contents_to_show = []
    try:
        all_contents = ContentsService().get_all_contents()
        for content in all_contents:
            contents_to_show.append({
                'id': content.id,
                'title_name': content.titulo,
                'description': content.contenido,
                'grade_level': content.nivel_grado,
                'topic': content.nombre_tema,
            })
            
        topics = TopicsService().get_all_topics()
        selection_topics = [
            {
                'id': topic.id,
                'name': topic.nombre,
            } for topic in topics
        ]
    except ValueError as e:
        error = str(e.__str__())

    return render_template(
        'content_management/contents.html',
        contents=contents_to_show,
        error=error,
        message=message,
        selection_topics=selection_topics
    )

@app.route("/contents/<int:content_id>", methods=["GET", "POST"])
def content_by_id(content_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    content: Contenido|None = None

    method = request.form.get('_method', 'GET')
    if method == 'PATCH':
        return edit_content(content_id)
    elif method == 'DELETE':
        return delete_content(content_id)

    if request.method == 'GET' or method == 'GET':
        content = ContentsService().get_content_by_id(content_id)

    return jsonify({
        'id': content.id,
        'topic_id': content.id_tema,
        'content_name': content.titulo,
        'content_description': content.contenido,
        'grade_level': content.nivel_grado,
    }) if content else None

def edit_content(content_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        content_name = request.form['edit_content_name']
        content_description = request.form['edit_content_description']
        topic_id = request.form['edit_topic_id']
        grade_level = request.form['edit_grade_level']
        message = ContentsService().update_content(
            content_id, topic_id, content_name, content_description, grade_level
        ).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('contents', error=error, message=message))

def delete_content(content_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        message = ContentsService().delete_content(content_id).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('contents', error=error, message=message))
