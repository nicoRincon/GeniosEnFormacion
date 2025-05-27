from src.content_management.subjects.subject_service import SubjectsService
from database.Materias.Contenido import Contenido
from database.Materias.Materia import Materia
from database.Materias.Tema import Tema
from src.db_connection import db

class TopicsService:
    def get_topic_by_id(self, topic_id: int) -> Tema:
        topic_by_id = (
            Tema.query
            .with_entities(
                Tema.id,
                Tema.id_materia,
                Tema.nombre,
                Tema.descripcion,
            )
            .filter(Tema.id == topic_id)
            .first()
        )
        if topic_by_id is None:
            raise ValueError(f"Tema con ID {topic_id} no existe.")
        return topic_by_id

    def get_all_topics(self) -> list[Tema]:
        all_topics = (
            Tema.query
            .with_entities(
                Tema.id,
                Materia.nombre.label('nombre_materia'),
                Tema.nombre,
                Tema.descripcion,
            )
            .all()
        )
        if len(all_topics) == 0:
            raise ValueError("No hay temas disponibles.")

        return all_topics

    def create_topic(self, subject_id: int, topic_name: str, topic_description: str|None):
        SubjectsService().get_subject_by_id(subject_id)
        self.validate_topic(topic_name, subject_id, None)

        new_topic = Tema(
            nombre = topic_name,
            descripcion = topic_description,
            id_materia = subject_id
        )
        db.session.add(new_topic)
        db.session.commit()
        return { 'message': f"Tema {topic_name} creado." }

    def update_topic(self, topic_id: int, subject_id: int, topic_name: str, topic_description: str):
        SubjectsService().get_subject_by_id(subject_id)

        topic_to_update: Tema = Tema.query.filter(Tema.id == topic_id).first()
        if topic_to_update is None:
            raise ValueError(f"Tema con ID {topic_id} no existe.")

        self.validate_topic(topic_name, subject_id, topic_id)

        topic_to_update.nombre = topic_name
        topic_to_update.descripcion = topic_description
        topic_to_update.id_materia = subject_id
        db.session.commit()
        return { 'message': f"Tema {topic_id} actualizado." }

    def delete_topic(self, topic_id: int):
        topic_to_delete: Tema = Tema.query.filter(Tema.id == topic_id).first()

        if topic_to_delete is None:
            raise ValueError(f"Tema con ID {topic_id} no existe.")

        contenido = Contenido.query.filter(Contenido.id_tema == topic_id).first()
        if contenido:
            raise ValueError(
                f"El tema {topic_to_delete.nombre} no se puede eliminar porque tiene contenido asociado."
            )

        db.session.delete(topic_to_delete)
        db.session.commit()
        return { 'message': f"Tema {topic_id} eliminado." }

    def validate_topic(self, topic_name: str, subject_id: int, topic_id: int|None):
        topic = Tema.query

        if topic_id is not None:
            topic = topic.filter(Tema.id != topic_id)
        topic = topic.filter(Tema.id_materia == subject_id)
        topic = topic.all()

        if topic and topic[0].nombre == topic_name:
            raise ValueError(f"Tema con el nombre: {topic_name}, ya existe para la materia seleccionada.")