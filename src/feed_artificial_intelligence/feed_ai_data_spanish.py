from sklearn.neighbors import KNeighborsClassifier
import random
from database.Materias.Contenido import Contenido
from database.Materias.Tema import Tema
from database.Materias.Materia import Materia
import joblib
import os

class FeedAIDataSpanish:
    def generate_knn_based_questions(self, content_id, model_path='static/data_ai/models/knn_model.pkl'):
        """
        Usa el modelo KNN para predecir la actividad para un contenido dado y genera preguntas/respuestas en formato JSON.
        Las preguntas y respuestas se generan de forma variada.
        """
        # Load the KNN model
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo no encontrado en {model_path}")
        model: KNeighborsClassifier = joblib.load(model_path)

        content: Contenido = Contenido.query.filter_by(id=content_id).first()
        if not content:
            return []

        topics: Tema = Tema.query.filter_by(id=content.id_tema).first()
        subject: Materia = Materia.query.filter_by(id=topics.id_materia).first() if topics else None

        subject_name = subject.nombre if subject else "Materia"
        topic_name = topics.nombre if topics else "Tema"
        content_name = content.titulo

        # Generate unique codes for subject, topic, and content
        subject_code = abs(hash(subject_name)) % 1000 if subject else 0
        topic_code = abs(hash(topic_name)) % 1000 if topics else 0
        content_code = abs(hash(content_name)) % 1000

        x_pred = [[subject_code, topic_code, content_code, content_id]]
        y_pred = model.predict(x_pred)
        predict_activity = str(y_pred[0])

        # Options and questions
        question_titles = [
            f"¿Cuál de las siguientes opciones está relacionada con el tema '{topic_name}'?",
            f"Selecciona el concepto que mejor describe el contenido '{content_name}'.",
            f"¿Qué opción corresponde a la materia '{subject_name}'?",
            f"¿Cuál es la respuesta correcta para el contenido '{content_name}'?"
        ]
        general_options = [
            [subject_name, topic_name, content_name],
            [content_name, "Concepto erróneo", "Ninguna de las anteriores"],
            [topic_name, "Otra materia", subject_name],
            [predict_activity, "Otra opción", "No corresponde"]
        ]
        correct_answers = [
            [topic_name],
            [content_name],
            [subject_name],
            [predict_activity]
        ]

        questions = []
        for _ in range(3):
            idx = random.randint(0, len(question_titles)-1)
            questions.append({
                "title": question_titles[idx],
                "options": general_options[idx],
                "correct_options": correct_answers[idx],
                "is_multiple_selection": False,
                "can_be_open_ended": False,
                "open_ended_response": ""
            })

        # Pregunta abierta personalizada
        questions.append({
            "title": f"Explica brevemente el tema '{topic_name}' en tus propias palabras.",
            "options": [],
            "correct_options": [],
            "is_multiple_selection": False,
            "can_be_open_ended": True,
            "open_ended_response": f"El tema '{topic_name}' trata sobre aspectos importantes de la materia '{subject_name}'."
        })

        return questions