from src.content_management.activity_types.activity_types_service import ActivityTypesService
from src.content_management.contents.contents_service import ContentsService
from src.content_management.activities.activities_service import ActivitiesService
from database.Materias.Actividad import Actividad
from src.db_connection import app
from flask import redirect, render_template, url_for, request, session
from flask import jsonify

@app.route("/activities", methods=["POST"])
def create_activities():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    if request.method == 'POST':
        content_id = request.form['content_id']
        activity_type_id = request.form['activity_type_id']
        content = request.form['questions_json']
        try:
            message = ActivitiesService().create_activity(
                content_id,
                activity_type_id,
                content
            ).get('message', None)
        except ValueError as e:
            error = str(e.__str__())

    return redirect(url_for('activities', error=error, message=message))

@app.route("/activities", methods=["GET"])
def activities():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    activities_to_show = []
    try:
        all_activities = ActivitiesService().get_all_activities()
        for activity in all_activities:
            activities_to_show.append({
                'id': activity.id,
                'content_name': activity.nombre_contenido,
                'activity_type': activity.tipo_actividad,
                'content': activity.contenido,
            })

        activity_types = ActivityTypesService().get_all_activity_types()
        contents = ContentsService().get_all_contents()

        selection_activity_types = [
            {
                'id': activity_type.id,
                'name': activity_type.tipo_actividad,
            } for activity_type in activity_types
        ]
        selection_contents = [
            {
                'id': content.id,
                'name': content.titulo,
            } for content in contents
        ]
    except ValueError as e:
        error = str(e.__str__())

    return render_template(
        'content_management/activities.html',
        activities=activities_to_show,
        error=error,
        message=message,
        selection_activity_types=selection_activity_types,
        selection_contents=selection_contents
    )

@app.route("/activities/<int:activity_id>", methods=["GET", "POST"])
def activity_by_id(activity_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    activity: Actividad|None = None

    method = request.form.get('_method', 'GET')
    if method == 'PATCH':
        return edit_activity(activity_id)
    elif method == 'DELETE':
        return delete_activity(activity_id)

    if request.method == 'GET' or method == 'GET':
        activity = ActivitiesService().get_activity_by_id(activity_id)

    return jsonify({
        'id': activity.id,
        'content_id': activity.id_contenido,
        'activity_type_id': activity.id_tipo_actividad,
        'questions_json': activity.contenido,
    }) if activity else None

def edit_activity(activity_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        activity_type_id = request.form['edit_activity_type_id']
        content_id = request.form['edit_content_id']
        content = request.form['edit_questions_json']
        message = ActivitiesService().update_activity(
            activity_id, content_id, activity_type_id, content
        ).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('activities', error=error, message=message))

def delete_activity(activity_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    message = None
    try:
        message = ActivitiesService().delete_activity(activity_id).get('message', None)
    except ValueError as e:
        error = str(e.__str__())

    return redirect(url_for('activities', error=error, message=message))
