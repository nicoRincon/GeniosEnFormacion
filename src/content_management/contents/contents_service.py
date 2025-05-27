from src.content_management.topics.topics_service import TopicsService
from database.Materias.Actividad import Actividad
from database.Materias.Contenido import Contenido
from database.Materias.Tema import Tema
from src.db_connection import db

class ContentsService:
    def get_content_by_id(self, content_id: int) -> Contenido:
        content_by_id = (
            Contenido.query
            .with_entities(
                Contenido.id,
                Contenido.id_tema,
                Contenido.titulo,
                Contenido.contenido,
                Contenido.nivel_grado,
            )
            .filter(Contenido.id == content_id)
            .first()
        )
        if content_by_id is None:
            raise ValueError(f"Contenido con ID {content_id} no existe.")
        return content_by_id

    def get_all_contents(self) -> list[Contenido]:
        all_contents = (
            Contenido.query
            .with_entities(
                Contenido.id,
                Tema.nombre.label('nombre_tema'),
                Contenido.titulo,
                Contenido.contenido,
                Contenido.nivel_grado,
            )
            .join(Contenido.tema)
            .all()
        )
        if len(all_contents) == 0:
            raise ValueError("No hay contenidos disponibles.")

        return all_contents

    def create_content(self, topic_id: int, content_title: str, content: str, grade_level: int):
        TopicsService().get_topic_by_id(topic_id)
        self.validate_content(content_title, topic_id, None)

        new_content = Contenido(
            titulo = content_title,
            contenido = content,
            nivel_grado = grade_level,
            id_tema = topic_id
        )
        db.session.add(new_content)
        db.session.commit()
        return { 'message': f"Contenido {content_title} creado." }

    def update_content(
        self,
        content_id: int,
        topic_id: int,
        content_name: str,
        content: str,
        grade_level: int
    ):
        TopicsService().get_topic_by_id(topic_id)

        content_to_update: Contenido = Contenido.query.filter(Contenido.id == content_id).first()
        if content_to_update is None:
            raise ValueError(f"Contenido con ID {content_id} no existe.")

        self.validate_content(content_name, topic_id, content_id)

        content_to_update.titulo = content_name
        content_to_update.contenido = content
        content_to_update.id_tema = topic_id
        content_to_update.nivel_grado = grade_level
        db.session.commit()
        return { 'message': f"Contenido {content_id} actualizado." }

    def delete_content(self, content_id: int):
        content_to_delete: Contenido = Contenido.query.filter(Contenido.id == content_id).first()

        if content_to_delete is None:
            raise ValueError(f"Contenido con ID {content_id} no existe.")

        contenido = Actividad.query.filter(Actividad.id_contenido == content_id).first()
        if contenido:
            raise ValueError(
                f"El contenido {content_to_delete.titulo} no se puede eliminar porque tiene actividades asociadas"
            )

        db.session.delete(content_to_delete)
        db.session.commit()
        return { 'message': f"Contenido {content_id} eliminado." }

    def validate_content(self, content_name: str, topic_id: int, content_id: int|None):
        content = Contenido.query
        if content_id is not None:
            content = content.filter(Contenido.id != content_id)

        content = content.filter(Contenido.id_tema == topic_id)
        content = content.all()

        if content and content[0].titulo == content_name:
            raise ValueError(f"Contenido con el nombre: {content_name}, ya existe para el tema seleccionado.")