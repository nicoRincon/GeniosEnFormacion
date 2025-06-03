from flask import jsonify, session, request, render_template
from src.ai_component.activity_generator_open_ai import ActivityGeneratorOpenAI
from src.ai_component.data_preprocessing import AiComponent
from src.db_connection import app


@app.route('/recommended_content_by_user', methods=['GET'])
def recommended_content_by_user():
    return jsonify(AiComponent().recommend_content())

@app.route('/clear_recommended_content_by_user', methods=['DELETE'])
def clear_recommended_content_by_user():
    AiComponent.clear_all_models()
    return jsonify({"message": "User models cleared successfully."})

@app.route('/recommended_activity_by_user', methods=['GET'])
def recommended_activity_by_user():
    try:
        ai_component = AiComponent()
        # Obtiene las recomendaciones
        recommendations = ai_component.recommend_content()

        if not recommendations or "error" in recommendations:
            return recommendations

        # Inicializa el generador de actividades
        activity_generator = ActivityGeneratorOpenAI()

        # Genera actividades para cada recomendación
        enriched_recommendations = []
        for rec in recommendations:
            content_id = rec.get('id_contenido')
            if content_id:
                activities = activity_generator.generate_activity(content_id)
                rec['activities_suggested'] = activities

            enriched_recommendations.append(rec)

        return {
            "success": True,
            "contents_with_activities": enriched_recommendations
        }

    except Exception as e:
        user_id = ai_component.get_user_id()
        print(f"Error generando actividades para usuario {user_id}: {e}")
        return {"error": f"Error al generar actividades: {str(e)}"}

@app.route('/submit_ai_activity', methods=['POST'])
def submit_ai_activity():
    if 'username' not in session:
        return jsonify({"error": "No autenticado"}), 401
    
    try:
        data = request.get_json()
        content_id = data.get('content_id')
        answers = data.get('answers', {})
        evaluation = data.get('evaluation', {})

        user_id = session.get('user_id')

        print(f"Usuario {user_id} completó actividad para contenido {content_id}")
        print(f"Puntuación: {evaluation.get('percentage', 0)}%")
        print(f"Respuestas correctas: {evaluation.get('correct', 0)}/{evaluation.get('total', 0)}")

        return jsonify({
            "success": True,
            "message": "Actividad guardada correctamente",
            "evaluation": evaluation
        })

    except Exception as e:
        print(f"Error guardando actividad: {e}")
        return jsonify({
            "success": False,
            "error": f"Error guardando actividad: {str(e)}"
        }), 500

@app.route('/get-ai-activity', methods=['GET'])
def get_ai_activity():
    return render_template('activities/ai_activities.html')