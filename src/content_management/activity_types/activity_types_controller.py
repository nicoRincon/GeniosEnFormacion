from src.content_management.activity_types.activity_types_service import ActivityTypesService
from src.db_connection import app
from flask import redirect, url_for, request, session
from flask import jsonify

@app.route("/activity_types", methods=["GET"])
def activity_types():
    if 'username' not in session:
        return redirect(url_for('login'))

    message = request.args.get('message', None)
    error = request.args.get('error', None)
    activities_to_show = []
    try:
        all_topics = ActivityTypesService().get_all_activity_types()
        for topic in all_topics:
            activities_to_show.append({
                'id': topic.id,
                'activity_type': topic.tipo_actividad,
                'weight': topic.peso
            })
    except ValueError as e:
        error = str(e.__str__())

    return jsonify({
        'activity_types': activities_to_show,
        'error': error,
        'message': message
    })
