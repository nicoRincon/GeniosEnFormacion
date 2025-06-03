import os
import json
from openai import OpenAI
from database.Materias.Contenido import Contenido
from database.Materias.Tema import Tema
from database.Materias.Materia import Materia

class ActivityGeneratorOpenAI:
    def __init__(self):
        """Inicializa el generador con tu API key de OpenAI"""
        self.client = OpenAI(api_key = os.getenv("OPEN_AI_API_KEY"))
        print("Generador OpenAI inicializado correctamente")

    def generate_activity(self, content_id: int):
        """Genera actividades en formato HTML usando GPT-3.5"""
        content_info = self._get_content_info(content_id)
        if not content_info:
            return {"error": "Contenido no encontrado"}

        try:
            # Genera actividades con OpenAI
            activity_data = self._generate_with_openai(content_info)

            return {
                "success": True,
                "activity_data_json": activity_data["questions"],
                "content_info": content_info,
                "generated_by": "OpenAI GPT-3.5"
            }

        except Exception as e:
            print(f"Error con OpenAI: {e}")
            raise Exception(f"Error generando actividad: {str(e)}")

    def _get_content_info(self, content_id: int):
        """Obtiene información del contenido desde la BD"""
        try:
            content: Contenido = Contenido.query. \
                filter(Contenido.id == content_id). \
                join(Contenido.tema). \
                join(Tema.materia). \
                with_entities(
                    Contenido.nivel_grado,
                    Contenido.contenido,
                    Contenido.titulo,
                    Materia.nombre.label('nombre_materia'),
                    Tema.nombre.label('nombre_tema'),
                ). \
                first()
            if not content:
                return None

            return {
                'id': content_id,
                'titulo': content.titulo,
                'contenido': content.contenido,
                'nivel_grado': content.nivel_grado,
                'tema': content.nombre_tema,
                'materia': content.nombre_materia
            }
        except Exception as e:
            print(f"Error obteniendo info del contenido: {e}")
            return None

    def _generate_with_openai(self, content_info):
        """Genera actividades usando OpenAI GPT-3.5"""
        prompt = self._build_educational_prompt(content_info)

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto pedagogo que crea actividades educativas excelentes para estudiantes. Siempre respondes en formato JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1200,
            temperature=0.7
        )

        # Extrae y procesa la respuesta
        ai_response = response.choices[0].message.content
        return self._parse_openai_response(ai_response)


    def _build_educational_prompt(self, content_info):
        """Construye el prompt educativo para OpenAI"""

        materia = content_info['materia']
        tema = content_info['tema']
        titulo = content_info['titulo']
        nivel = content_info['nivel_grado']
        descripcion = content_info.get('contenido', '')

        prompt = f"""
            Crea una actividad educativa para estudiantes de grado {nivel} sobre:

            **Materia:** {materia}
            **Tema:** {tema}
            **Contenido:** {titulo}
            **Descripción:** {descripcion}

            Genera exactamente 4 preguntas educativas apropiadas para el nivel:
            - 3 preguntas de selección múltiple (4 opciones cada una)
            - 1 pregunta abierta para reflexión

            IMPORTANTE: Responde SOLO con un JSON válido en este formato exacto:

            {{"questions": [
                {{
                    "type": "multiple",
                    "question": "Pregunta aquí",
                    "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                    "correct_answer": ["Opción correcta"],
                    "explanation": "Breve explicación de por qué es correcta"
                }},
                {{
                    "type": "open",
                    "question": "Pregunta abierta aquí",
                    "sample_answer": "Ejemplo de respuesta esperada",
                    "evaluation_criteria": "Criterios para evaluar la respuesta"
                }},
                {{
                    "type": "single",
                    "question": "Pregunta aquí",
                    "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                    "correct_answer": ["Opción correcta"],
                    "explanation": "Breve explicación de por qué es correcta"
                }}
            ]}}

            Asegúrate de que:
            - Las preguntas sean apropiadas para grado {nivel}
            - El lenguaje sea claro y simple
            - Las opciones incorrectas sean plausibles pero claramente incorrectas
            - La pregunta abierta fomente la reflexión y aplicación del conocimiento
        """

        return prompt

    def _parse_openai_response(self, response_text):
        """Procesa la respuesta de OpenAI y extrae el JSON"""
        try:
            # Limpia la respuesta para extraer solo el JSON
            response_text = response_text.strip()

            # Busca el JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                data = json.loads(json_text)

                # Valida que tenga la estructura esperada
                if "questions" in data and isinstance(data["questions"], list):
                    return {
                        "success": True,
                        "questions": data["questions"]
                    }
                else:
                    raise ValueError("Estructura de JSON inválida")
            else:
                raise ValueError("No se encontró JSON válido en la respuesta")

        except Exception as e:
            print(f"Error procesando respuesta de OpenAI: {e}")
            print(f"Respuesta recibida: {response_text[:200]}...")
            return {
                "success": False,
                "error": f"Error procesando respuesta: {str(e)}"
            }
