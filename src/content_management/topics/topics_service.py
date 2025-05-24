from database.Materias.Materia import Materia
from database.Materias.Tema import Tema
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Usuarios.Usuario import Usuario
from src.db_connection import db

class TopicsService:
    def get_topic_by_id(self, topic_id: int) -> Materia:
        topic_by_id = (
            Tema.query
            .with_entities(
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
            )
            .join(Materia.temas)
            .filter(Tema.id == topic_id)
            .first()
        )
        if topic_by_id is None:
            raise ValueError(f"Materia con ID {topic_id} no existe.")
        return topic_by_id

    def get_all_topics(self) -> list[Materia]:
        all_topics = (
            Materia.query
            .with_entities(
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
            )
            .all()
        )
        if len(all_topics) == 0:
            raise ValueError("No hay materias disponibles.")

        return all_topics

    def create_topic(self, topic_name: str, topic_description: str|None):
        self.validate_topic(topic_name, None)

        new_topic = Materia(nombre=topic_name, descripcion=topic_description)
        db.session.add(new_topic)
        db.session.commit()
        return { 'message': f"Materia {topic_name} creada." }

    def update_topic(self, topic_id: int, topic_name: str, topic_description: str):
        materia_to_update: Materia = Materia.query.filter(Materia.id == topic_id).first()
        if materia_to_update is None:
            raise ValueError(f"Materia with ID {topic_id} no existe.")

        self.validate_topic(topic_name, topic_id)

        materia_to_update.nombre = topic_name
        materia_to_update.descripcion = topic_description
        db.session.commit()
        return { 'message': f"Materia {topic_id} actualizada." }

    def delete_topic(self, topic_id: int):
        topic_to_delete = Materia.query.filter(Materia.id == topic_id).first()
        if topic_to_delete is None:
            raise ValueError(f"Materia con ID {topic_id} no existe.")

        user: Usuario = (
            Usuario.query
            .join(UsuarioMateria.usuarios)
            .filter(Usuario.id == topic_id)
            .first()
        )
        if user:
            raise ValueError(f"La materia {topic_id} no se puede eliminar porque tiene usuarios asociados.")

        db.session.delete(topic_to_delete)
        db.session.commit()
        return { 'message': f"Materia {topic_id} eliminada." }

    def validate_topic(self, topic_name: str, topic_id: int|None):
        topic = Materia.query

        if topic_id is not None:
            topic = topic.filter(Materia.id != topic_id)
        print(topic.statement)
        topic = topic.all()

        if topic and topic[0].nombre == topic_name:
            raise ValueError(f"Materia con el nombre: {topic_name}, ya existe.")

        return topic