from flask import jsonify
from src.ai_component.data_preprocessing import AiComponent
from src.db_connection import app


@app.route('/recommended_content_by_user', methods=['GET'])
def recommended_content_by_user():
    return jsonify(AiComponent().recommend_content())

@app.route('/clear_recommended_content_by_user', methods=['DELETE'])
def clear_recommended_content_by_user():
    AiComponent.clear_all_models()
    return jsonify({"message": "User models cleared successfully."})
